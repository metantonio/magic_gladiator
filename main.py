import json

class MagicGladiator:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.experience = 0
        self.max_hp = 110
        self.hp = self.max_hp
        self.strength = 26
        self.agility = 26
        self.stamina = 26
        self.energy = 26
        self.max_mana = 60
        self.mana = self.max_mana
        self.max_damage = (self.strength/4) + (self.energy/8)
        self.min_damage = (self.strength/6) + (self.energy/12)
        self.attack_rate_pvm = (self.level*5) + (self.agility*1.5) + (self.strength/4)
        self.attack_rate_pvp = (self.level*3) + (self.agility*3.5)
        self.defense = self.agility
        self.speed = self.agility/15
        self.speed_magic = self.agility/20
        self.defense_rate_pvm = self.agility/3
        self.defense_rate_pvp = self.agility*0.25 + self.level*2
        self.max_wizard_attack = self.energy/4
        self.min_wizardy_attack = self.energy/9
        self.ag_bar = (self.strength*0.2)+(self.agility*0.25)+(0.3*self.stamina)+(0.15*self.energy)
        self.min_elemental_damage = self.strength/10 + self.energy/14
        self.max_elemental_damage = self.strength/6 + self.energy/8
        self.elemental_defense = self.agility/5


    def level_up(self):
        self.level += 1
        self.max_hp += 1
        self.max_mana += 1
        self.hp = self.max_hp
        self.mana = self.max_mana
        self.strength += 2
        self.agility += 1
        self.stamina += 1
        self.energy += 2

    def increase_strength(self):
        self.strength += 1

    def increase_agility(self):
        self.agility += 1

    def increase_stamina(self):
        self.stamina += 1

    def increase_energy(self):
        self.energy += 1

    def calculate_damage(self, enemy_defense):
        base_damage = self.strength * 2
        damage = base_damage - enemy_defense
        return max(damage, 0)

    def calculate_defense(self, armor_defense):
        base_defense = self.agility + self.stamina
        defense = base_defense + armor_defense
        return defense

    def save_character(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.__dict__, file, indent=4)

    @classmethod
    def load_character(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        character = cls.__new__(cls)
        character.__dict__.update(data)
        return character

    def check_level_up(self, exp_table):
        if self.level < len(exp_table) and self.experience >= exp_table[self.level]["Experiencia_Necesaria"]:
            self.level_up()
            print(f"{self.name} has leveled up to level {self.level}!")

    def calculate_experience(self, enemy_level):
        base_exp = 100
        exp_gain = base_exp * (enemy_level / self.level)
        self.experience += exp_gain
        # Check if level up
        self.check_level_up(exp_table)


class Enemy:
    def __init__(self, name, level, max_hp, strength, agility, defense):
        self.name = name
        self.level = level
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.agility = agility
        self.defense = defense

    def attack(self):
        # Lógica para el ataque del enemigo
        pass

    def take_damage(self, damage):
        # Reducir los puntos de vida del enemigo basado en el daño recibido
        self.hp -= damage
        if self.hp <= 0:
            print(f"{self.name} has been defeated!")


# Función para cargar la tabla de experiencia desde un archivo de texto
def load_exp_table(filename):
    exp_table = []
    with open(filename, 'r') as file:
        next(file)  # Saltar la primera línea (encabezado)
        for line in file:
            level, exp_needed, exp_accumulated = line.strip().split('\t')
            exp_table.append({
                "Level": int(level),
                "Experiencia_Necesaria": int(exp_needed.replace(',', '')) if exp_needed != '-' else None,
                "Experiencia_Acumulada": int(exp_accumulated.replace(',', ''))  # Eliminar comas de números
            })
    return exp_table

# Ejemplo de uso
filename = "character_data.json"
exp_table_filename = "exp_table.txt"

# Intentar cargar el personaje desde el archivo
try:
    player1 = MagicGladiator.load_character(filename)
    print("Character loaded successfully!")
except FileNotFoundError:
    print("Creating a new character...")
    player1 = MagicGladiator("Player1")

# Cargar la tabla de experiencia
exp_table = load_exp_table(exp_table_filename)

# Mostrar los datos del personaje
print(f"Name: {player1.name}")
print(f"Level: {player1.level}")
print(f"Strength: {player1.strength}")
print(f"Agility: {player1.agility}")
print(f"Stamina: {player1.stamina}")
print(f"Energy: {player1.energy}")

# Incrementar experiencia para simular la adquisición de experiencia durante el juego
#player1.experience += 5000
# Ejemplo de uso
enemy1 = Enemy("Goblin", 3, 50, 8, 6, 2)
enemy2 = Enemy("Orc", 5, 80, 12, 8, 5)

enemy_level = 5
player1.calculate_experience(enemy1.level)
print(f"Experience: {player1.experience}")
print(f"Level: {player1.level}")

enemy_defense = 10
damage = player1.calculate_damage(enemy_defense)
print(f"Damage dealt to enemy: {damage}")

armor_defense = 5
defense = player1.calculate_defense(armor_defense)
print(f"Total defense: {defense}")


# Guardar los cambios del personaje
player1.save_character(filename)
print("Character data saved successfully!")
