from ursina import *
import random
from ursina.shaders import basic_lighting_shader as bls, lit_with_shadows_shader as lit

Entity.default_shader = lit

def update():
    global fuel, current_target_index

    if not plane: return

    # Hedef noktaya doğru uçağı hareket ettirin
    target_point = target_points[current_target_index]
    # direction = Vec3(target_point[0] - plane.x, target_point[1] - plane.y, target_point[2] - plane.z)
    plane.look_at_2d(Vec3(target_point), axis="y")
    # direction.normalize()
    if plane.fly : plane.position += plane.forward * 0.05  # Uçak hızı ayarlayın

    # Hedef noktaya ulaşıldığında bir sonraki hedefe geçin
    if distance(plane.position, target_point) < 0.1:
        current_target_index = (current_target_index + 1) % len(target_points)

    # # Rastgele hareket için uçağı güncelleyin
    # plane.x += random.uniform(-0.1, 0.1)
    # plane.z += random.uniform(-0.1, 0.1)

    # Yakıtı azaltın
    fuel -= 0.1  # Örneğin, her güncelleme döngüsünde 0.1 birim yakıt azalıyor

    # Yakıt çubuğunu güncelleyin
    health_percentage = fuel / 100.0  # Sağlık çubuğunu yakıt miktarına göre güncelleyin
    health_bar.scale_x = max(health_percentage, 0)*7  # Sağlık çubuğu negatif değer almasın

    # Yakıt tükendiğinde oyunu sonlandırın
    if fuel <= 0 and plane.fly:
        plane.animate('y', 0, duration=1)
        plane.fly = False



app = Ursina()

# Uçağınızı oluşturun veya içe aktarın
plane = Entity(model="Airplane.obj", texture="AirplaneBaked", y=15, fly=True, shader=bls)

# Sağlık çubuğunu oluşturun
health_bar = Entity(model='quad', scale=(7, .5), color=color.green, parent=plane, billboard=True)
health_bar.y = 1.5  # Sağlık çubuğunu uçağın üstüne yerleştirin

# Uçağın başlangıç yakıt miktarını ayarlayın
fuel = 100.0  # Örneğin, başlangıçta 100 birim yakıt

# Uçağın uçacağı 5 farklı hedef nokta belirleyin
target_points = [(300, 15, 300), (-300, 15, 300), (250, 15, -200), (-150, 15, -350), (0, 15, 0)]
current_target_index = 0

ground = Entity(model="plane", texture="grass", scale=200)

Sky()

EditorCamera()

sun = DirectionalLight() # yönlendirilmiş ışık 
sun.look_at((-1, -1, 1))

app.run()
