import pygame
import numpy as np
import math
import random

pygame.init()

# Configuration
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
CUBE_SIZE = 5  # Nombre de sous-cubes par dimension (5x5x5)
SUB_CUBE_SIZE = 20  # Taille d'un sous-cube en pixels
BUTTON_HEIGHT = 60

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER = (100, 100, 100)

class Camera:
    def __init__(self):
        self.distance = 300
        self.angle_x = 0.3
        self.angle_y = 0.3
        self.center = np.array([0, 0, 0])
    
    def rotate(self, dx, dy):
        self.angle_y += dx * 0.01
        self.angle_x += dy * 0.01
        self.angle_x = max(-math.pi/2 + 0.1, min(math.pi/2 - 0.1, self.angle_x))
    
    def zoom(self, delta):
        self.distance = max(100, min(800, self.distance + delta))
    
    def get_view_matrix(self):
        # Position de la caméra
        x = self.distance * math.cos(self.angle_x) * math.cos(self.angle_y)
        y = self.distance * math.sin(self.angle_x)
        z = self.distance * math.cos(self.angle_x) * math.sin(self.angle_y)
        
        camera_pos = np.array([x, y, z]) + self.center
        
        # Matrice de vue simplifiée
        forward = self.center - camera_pos
        forward = forward / np.linalg.norm(forward)
        
        up = np.array([0, 1, 0])
        right = np.cross(forward, up)
        right = right / np.linalg.norm(right)
        up = np.cross(right, forward)
        
        return camera_pos, forward, right, up

class SubCube:
    def __init__(self, x, y, z, size):
        self.grid_pos = (x, y, z)
        self.world_pos = np.array([
            (x - CUBE_SIZE//2) * size,
            (y - CUBE_SIZE//2) * size,
            (z - CUBE_SIZE//2) * size
        ])
        self.size = size
        self.is_white = random.choice([True, False])
        self.vertices = self._generate_vertices()
        self.faces = [
            [0, 1, 2, 3],  # front
            [4, 5, 6, 7],  # back
            [0, 1, 5, 4],  # bottom
            [2, 3, 7, 6],  # top
            [0, 3, 7, 4],  # left
            [1, 2, 6, 5]   # right
        ]
    
    def _generate_vertices(self):
        s = self.size / 2
        vertices = []
        for dx in [-s, s]:
            for dy in [-s, s]:
                for dz in [-s, s]:
                    vertices.append(self.world_pos + np.array([dx, dy, dz]))
        return vertices
    
    def toggle_color(self):
        self.is_white = not self.is_white
    
    def get_color(self):
        return WHITE if self.is_white else BLACK

class Cube3D:
    def __init__(self):
        self.sub_cubes = []
        self.camera = Camera()
        self._generate_sub_cubes()
    
    def _generate_sub_cubes(self):
        self.sub_cubes = []
        for x in range(CUBE_SIZE):
            for y in range(CUBE_SIZE):
                for z in range(CUBE_SIZE):
                    sub_cube = SubCube(x, y, z, SUB_CUBE_SIZE)
                    self.sub_cubes.append(sub_cube)
    
    def randomize_colors(self):
        for sub_cube in self.sub_cubes:
            sub_cube.is_white = random.choice([True, False])
    
    def project_point(self, point, camera_pos, forward, right, up):
        # Transformation vers l'espace caméra
        relative = point - camera_pos
        cam_x = np.dot(relative, right)
        cam_y = np.dot(relative, up)
        cam_z = np.dot(relative, forward)
        
        if cam_z <= 0:
            return None
        
        # Projection perspective
        focal_length = 400
        screen_x = SCREEN_WIDTH // 2 + (cam_x * focal_length) / cam_z
        screen_y = SCREEN_HEIGHT // 2 - (cam_y * focal_length) / cam_z
        
        return (int(screen_x), int(screen_y)), cam_z
    
    def render(self, screen):
        camera_pos, forward, right, up = self.camera.get_view_matrix()
        
        # Calculer les projections et trier par profondeur
        rendered_faces = []
        
        for sub_cube in self.sub_cubes:
            projected_vertices = []
            depths = []
            
            for vertex in sub_cube.vertices:
                projection = self.project_point(vertex, camera_pos, forward, right, up)
                if projection:
                    projected_vertices.append(projection[0])
                    depths.append(projection[1])
                else:
                    projected_vertices.append(None)
                    depths.append(float('inf'))
            
            # Calculer les faces visibles
            for i, face in enumerate(sub_cube.faces):
                if all(projected_vertices[j] is not None for j in face):
                    face_vertices = [projected_vertices[j] for j in face]
                    avg_depth = sum(depths[j] for j in face) / len(face)
                    
                    # Test de visibilité basique (face normale)
                    v1 = np.array(face_vertices[1]) - np.array(face_vertices[0])
                    v2 = np.array(face_vertices[2]) - np.array(face_vertices[0])
                    normal = np.cross(v1, v2)
                    
                    if normal > 0:  # Face visible
                        rendered_faces.append((avg_depth, face_vertices, sub_cube))
        
        # Trier par profondeur (plus loin en premier)
        rendered_faces.sort(key=lambda x: x[0], reverse=True)
        
        # Dessiner les faces
        for depth, vertices, sub_cube in rendered_faces:
            color = sub_cube.get_color()
            if len(vertices) >= 3:
                try:
                    pygame.draw.polygon(screen, color, vertices)
                    pygame.draw.polygon(screen, GRAY, vertices, 1)
                except:
                    pass
    
    def get_clicked_cube(self, mouse_pos):
        camera_pos, forward, right, up = self.camera.get_view_matrix()
        
        closest_cube = None
        closest_distance = float('inf')
        
        for sub_cube in self.sub_cubes:
            # Projeter le centre du sous-cube
            center_projection = self.project_point(sub_cube.world_pos, camera_pos, forward, right, up)
            
            if center_projection:
                screen_pos, depth = center_projection
                distance = math.sqrt((mouse_pos[0] - screen_pos[0])**2 + (mouse_pos[1] - screen_pos[1])**2)
                
                # Zone de clic approximative
                if distance < SUB_CUBE_SIZE and depth < closest_distance:
                    closest_distance = depth
                    closest_cube = sub_cube
        
        return closest_cube

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cube 3D Interactif")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    cube = Cube3D()
    
    # Variables pour la souris
    mouse_down = False
    last_mouse_pos = None
    
    # Bouton Init
    button_rect = pygame.Rect(SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT - BUTTON_HEIGHT + 10, 100, 40)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if button_rect.collidepoint(event.pos):
                        cube.randomize_colors()
                    else:
                        if event.pos[1] < SCREEN_HEIGHT - BUTTON_HEIGHT:
                            clicked_cube = cube.get_clicked_cube(event.pos)
                            if clicked_cube:
                                clicked_cube.toggle_color()
                        mouse_down = True
                        last_mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down and last_mouse_pos:
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    cube.camera.rotate(dx, dy)
                    last_mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEWHEEL:
                cube.camera.zoom(-event.y * 20)
        
        # Rendu
        screen.fill((50, 50, 50))
        
        # Dessiner le cube
        cube.render(screen)
        
        # Dessiner l'interface
        pygame.draw.rect(screen, (30, 30, 30), (0, SCREEN_HEIGHT - BUTTON_HEIGHT, SCREEN_WIDTH, BUTTON_HEIGHT))
        
        # Bouton Init
        mouse_pos = pygame.mouse.get_pos()
        button_color = BUTTON_HOVER if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_rect)
        pygame.draw.rect(screen, WHITE, button_rect, 2)
        
        text = font.render("INIT", True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)
        
        # Instructions
        instructions = [
            "Clic gauche: sélectionner un sous-cube",
            "Glisser: tourner la caméra",
            "Molette: zoomer/dézoomer"
        ]
        
        small_font = pygame.font.Font(None, 24)
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, WHITE)
            screen.blit(text, (10, 10 + i * 25))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()