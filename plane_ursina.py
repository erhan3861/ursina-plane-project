from ursina import *
import random
from ursina.shaders import basic_lighting_shader as bls, lit_with_shadows_shader as lit
from ursina import curve

Entity.default_shader = lit

def update():
    global fuel, current_target_index

    if not plane : return

    # Hedef noktaya doğru uçağı hareket ettirin
    target_point = target_points[current_target_index]
    
    plane.look_at_2d(Vec3(target_point), axis="y")
    
    if plane.fly : plane.position += plane.forward * 0.05  # Uçak hızı ayarlayın

    # Hedef noktaya ulaşıldığında bir sonraki hedefe geçin
    if distance(plane.position, target_point) < 0.1:
        current_target_index = (current_target_index + 1) % len(target_points)

    # Yakıtı azaltın
    fuel -= 0.1  # Örneğin, her güncelleme döngüsünde 0.1 birim yakıt azalıyor

    # Yakıt çubuğunu güncelleyin
    health_percentage = fuel / 100.0  # Sağlık çubuğunu yakıt miktarına göre güncelleyin
    if health_percentage < 0.002:
        health_percentage = 0.01

    print("health_percentage = ", health_percentage)
    health_bar.scale_x = health_percentage * 7  # Sağlık çubuğu negatif değer almasın

    # Yakıt tükendiğinde oyunu sonlandırın
    if fuel <= 0 and plane.fly:
        print("hata1")
        plane.animate('y', 0, duration=3, curve = curve.linear)
        invoke(destroy, plane, delay=5)
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
target_points = [(3, 15, 3), (-3, 15, 3), (25, 15, -20), (-15, 15, -3), (0, 15, 0)]
current_target_index = 0

ground = Entity(model="plane", texture="grass", scale=200)

Sky()

EditorCamera(y=30)

sun = DirectionalLight() # yönlendirilmiş ışık 
sun.look_at((-1, -1, 1))

app.run()
