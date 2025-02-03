import random
from pygame import Rect
from pgzero.actor import Actor
from pgzero.clock import schedule
import pgzrun

#Constantes do Jogo
WIDTH, HEIGHT = 900, 600
gameState = 'menu'
sounds_enabled = True  

#Elementos Visuais do Jogo
background3 = Actor('battleground3.png')
floor = Actor('chao.png')
player = Actor('hero_idle_0.png')
enemy = Actor('enemy_idle0.png', anchor=('center', 'bottom'))

#Posicionamento Inicial
floor.pos = (450, 550)
player.pos = (50, 440)
enemy.pos = (800, 500)

#Botões do Menu Principal
button_start = Rect(350, 200, 200, 50) 
button_sound = Rect(350, 275, 200, 50)
button_exit = Rect(350, 350, 200, 50)
button_restart = Rect(350, 425, 200, 50)

#Estados do Jogo
playerDead = False
enemyDead = False
jumping = False
attacking = False
enemyAttacking = False
gameMessage = None

#Parâmetros de Animação e Mecânicas
attackFrame = 0
playerDeathFrame = 0
enemyDeathFrame = 0
runFrame = 0
enemyWalkFrame = 0
enemyAttackFrame = 0

#Atributos do Jogador e do Inimigo
playerHealth = 100
enemyHealth = 50
playerDamage = 8
enemyDamage = 5
jumps = 2
enemyAttackCooldown = 1.0
walkSpeed = 0.08

#Controle de Animação e Direções
animationEnabled = True
canEnemyAttack = True
playerDirection = "right"
enemyDirection = "left"

playerIdle = {'right': ['hero_idle_0.png', 'hero_idle_1.png', 'hero_idle_2.png', 'hero_idle_3.png', 'hero_idle_4.png', 'hero_idle_5.png'],
              'left': ['hero_idle_left0.png', 'hero_idle_left1.png', 'hero_idle_left2.png', 'hero_idle_left3.png', 'hero_idle_left4.png', 'hero_idle_left5.png']}

playerRun = {'right': ['hero_run_0.png', 'hero_run_1.png', 'hero_run_2.png', 'hero_run_3.png', 'hero_run_4.png', 'hero_run_5.png', 'hero_run_6.png', 'hero_run_7.png'],
             'left': ['hero_run_left0.png', 'hero_run_left1.png', 'hero_run_left2.png', 'hero_run_left3.png', 'hero_run_left4.png', 'hero_run_left5.png', 'hero_run_left6.png', 'hero_run_left7.png']}

playerJump = {'right': ['hero_jump_0.png', 'hero_jump_1.png', 'hero_jump_2.png', 'hero_jump_3.png', 'hero_jump_4.png', 'hero_jump_5.png', 'hero_jump_6.png', 'hero_jump_7.png', 'hero_jump_8.png', 'hero_jump_9.png', 'hero_jump_10.png', 'hero_jump_11.png' ],
              'left': ['hero_jump_left0.png', 'hero_jump_left1.png', 'hero_jump_left2.png', 'hero_jump_left3.png', 'hero_jump_left4.png', 'hero_jump_left5.png', 'hero_jump_left6.png', 'hero_jump_left7.png', 'hero_jump_left8.png', 'hero_jump_left9.png', 'hero_jump_left10.png', 'hero_jump_left11.png']}

playerAttack = {'right': ['hero_attack_0.png', 'hero_attack_1.png', 'hero_attack_2.png', 'hero_attack_3.png', 'hero_attack_4.png', 'hero_attack_5.png'],
                'left': ['hero_attack_left0.png', 'hero_attack_left1.png', 'hero_attack_left2.png', 'hero_attack_left3.png', 'hero_attack_left4.png', 'hero_attack_left5.png']}

playerDeath = {'right': ['hero_die_0.png', 'hero_die_1.png', 'hero_die_2.png'],
                'left': ['hero_die_left0.png', 'hero_die_left1.png', 'hero_die_left2.png']}

enemyIdle = {'right': ['enemy_idle0.png', 'enemy_idle1.png', 'enemy_idle2.png', 'enemy_idle3.png', 'enemy_idle4.png'],
             'left': ['enemy_idle_left0.png', 'enemy_idle_left1.png', 'enemy_idle_left2.png', 'enemy_idle_left3.png', 'enemy_idle_left4.png']}

enemyAttack = {'right': ['enemy_attack0.png', 'enemy_attack1.png', 'enemy_attack2.png', 'enemy_attack3.png', 'enemy_attack4.png', 'enemy_attack5.png', 'enemy_attack6.png', 'enemy_attack7.png', 'enemy_attack8.png'],
               'left': ['enemy_attack_left0.png', 'enemy_attack_left1.png', 'enemy_attack_left2.png', 'enemy_attack_left3.png', 'enemy_attack_left4.png', 'enemy_attack_left5.png', 'enemy_attack_left6.png', 'enemy_attack_left7.png', 'enemy_attack_left8.png']}

enemyDeath = {'right': ['enemy_die_0.png', 'enemy_die_1.png', 'enemy_die_2.png', 'enemy_die_3.png'],
              'left': ['enemy_die_left0.png', 'enemy_die_left1.png', 'enemy_die_left2.png', 'enemy_die_left3.png']}

enemyWalk = {'right': ['enemy_walk_0.png', 'enemy_walk_1.png', 'enemy_walk_2.png', 'enemy_walk_3.png', 'enemy_walk_4.png', 'enemy_walk_5.png'],
             'left': ['enemy_walk_left0.png', 'enemy_walk_left1.png', 'enemy_walk_left2.png', 'enemy_walk_left3.png', 'enemy_walk_left4.png', 'enemy_walk_left5.png']}

def update():
    global gameState

    if gameState == 'menu':
        return  

    elif gameState == 'play':
        move_player()
        enemy_follow_player()
        if keyboard.ESCAPE:  
            gameState = 'menu'
            sounds.background_music.stop()  

def toggle_sounds():
    global sounds_enabled

    sounds_enabled = not sounds_enabled

    if sounds_enabled:
        sounds.background_music.play(-1)  
    else:
        sounds.background_music.stop()  

def on_mouse_down(pos):
    global gameState, sounds_enabled

    if gameState == 'menu':  
        sounds.background_music.stop()
        if button_start.collidepoint(pos):
            gameState = 'play'  
            if sounds_enabled:  
                sounds.background_music.play(-1)
        elif button_sound.collidepoint(pos):
            toggle_sounds()  
        elif button_exit.collidepoint(pos):
            exit()  
        elif button_restart.collidepoint(pos):  
            reset_game()  

def draw():
    screen.clear()

    if gameState == 'menu':
        screen.draw.text("Menu Principal", center=(WIDTH / 2, 100), fontsize=50, color="white")
        screen.draw.filled_rect(button_start, "gray")
        screen.draw.filled_rect(button_sound, "gray")
        screen.draw.filled_rect(button_exit, "gray")
        screen.draw.filled_rect(button_restart, "gray")

        screen.draw.text("Começar Jogo", center=button_start.center, fontsize=30, color="white")
        screen.draw.text("Música: " + ("Ligada" if sounds_enabled else "Desligada"), center=button_sound.center, fontsize=30, color="white")
        screen.draw.text("Sair", center=button_exit.center, fontsize=30, color="white")
        screen.draw.text("Reiniciar Jogo", center=button_restart.center, fontsize=30, color="white")

    elif gameState == 'play':
        background3.draw()
        floor.draw()
        player.draw()
        enemy.draw()
        draw_health_bars()

    if gameMessage:
        screen.fill((0, 0, 0))
        screen.draw.text(gameMessage, center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color="white")
        return  

def move_player():
    global jumping, jumps, playerDirection, attacking, runFrame

    if playerDead:
        return

    runSpeed = 0.07  
    moving = False

    if keyboard.d and player.x < WIDTH:
        playerDirection = "right"
        if not attacking:
            player.image = playerRun[playerDirection][runFrame]
            runFrame = (runFrame + 1) % len(playerRun[playerDirection])
            schedule(lambda: move_player(), runSpeed)
        player.x += 5
        moving = True

    elif keyboard.a and player.x > 0:
        playerDirection = "left"
        if not attacking:
            player.image = playerRun[playerDirection][runFrame]
            runFrame = (runFrame + 1) % len(playerRun[playerDirection])
            schedule(lambda: move_player(), runSpeed)
        player.x -= 5
        moving = True

    if not moving and not attacking and not jumping:
        player.image = playerIdle[playerDirection][0]

    if keyboard.k and not attacking:
        attacking = True
        animate_attack()

    if keyboard.space and not jumping:
        jumping = True
        jumps -= 1
        if sounds_enabled:
            sounds.herojump.play() 
        player.image = playerJump[playerDirection][random.randint(0, len(playerJump[playerDirection]) - 1)]
        player.y -= 100
        schedule(land_player, 0.5)

    if not player.colliderect(floor):
        player.y += 5
        jumping = True
    else:
        jumping = False
        jumps = 2

def animate_attack():
    global attackFrame, attacking, enemyHealth, enemyDead, enemyDeathFrame

    if enemyDead: 
        attacking = False
        return

    if attackFrame == 0 and sounds_enabled:
        sounds.heroattack.play()

    if attackFrame < len(playerAttack[playerDirection]):
        player.image = playerAttack[playerDirection][attackFrame]
        attackFrame += 1
        schedule(animate_attack, 0.05)
    else:
        attackFrame = 0
        attacking = False
        player.image = playerIdle[playerDirection][0]

        if abs(player.x - enemy.x) < 50 and not enemyDead:
            enemyHealth -= playerDamage
            if sounds_enabled:
                sounds.enemyhurt.play()
            if enemyHealth <= 0:
                enemyHealth = 0
                enemyDead = True
                enemyDeathFrame = 0
                animate_enemy_death()

def land_player():
    global jumping
    jumping = False
    player.image = playerIdle[playerDirection][0]

def animate_player_death():
    global playerDeathFrame, playerDead, gameMessage

    if playerDeathFrame == 0 and sounds_enabled:
        sounds.herodie.play()

    if playerDeathFrame < len(playerDeath[playerDirection]):
        player.image = playerDeath[playerDirection][playerDeathFrame]
        playerDeathFrame += 1
        schedule(animate_player_death, 0.12)
    else:
        gameMessage = "you lose!"
        screen.clear()
        schedule(return_to_menu, 2) 

def animate_enemy_attack():
    global enemyAttackFrame, enemyAttacking

    if enemyAttackFrame < len(enemyAttack[enemyDirection]):
        enemy.image = enemyAttack[enemyDirection][enemyAttackFrame]
        enemyAttackFrame += 1
        schedule(animate_enemy_attack, 0.12)  
    else:
        enemyAttackFrame = 0
        enemyAttacking = False 

        if abs(enemy.x - player.x) > 50:  
            animate_enemy_walk()  
        else:
            enemy.image = enemyIdle[enemyDirection][0] 

def enable_enemy_attack():
    global canEnemyAttack
    canEnemyAttack = True
def enemy_follow_player():
    global enemyDirection, playerDead, playerHealth, enemyAttacking, canEnemyAttack

    if enemyDead:
        return

    if abs(enemy.x - player.x) < 50 and not playerDead:
        if not enemyAttacking and canEnemyAttack:
            enemyAttacking = True
            canEnemyAttack = False
            animate_enemy_attack()
            playerHealth -= enemyDamage
            if sounds_enabled:
                sounds.herodie.play()
            if playerHealth <= 0:
                playerHealth = 0
                playerDead = True
                animate_player_death()

            schedule(enable_enemy_attack, enemyAttackCooldown)
    else:
        if enemy.x < player.x:
            enemyDirection = "right"
            enemy.x += 2
        elif enemy.x > player.x:
            enemyDirection = "left"
            enemy.x -= 2
        if not enemyAttacking and enemyWalkFrame == 0:
            animate_enemy_walk()

    enemy.y = floor.pos[1] - 50 

def animate_enemy_walk():
    global enemyWalkFrame

    if enemyDead or enemyAttacking:
        return

    enemy.image = enemyWalk[enemyDirection][enemyWalkFrame]
    enemyWalkFrame = (enemyWalkFrame + 1) % len(enemyWalk[enemyDirection])  
    schedule(animate_enemy_walk, 0.12)

def animate_enemy_death():
    global enemyDeathFrame, enemyDead, gameMessage

    if enemyDeathFrame == 0 and sounds_enabled:
        enemyDead = True
        sounds.enemydie.play() 
        enemy.image = enemyDeath[enemyDirection][0]

    if enemyDeathFrame < len(enemyDeath[enemyDirection]):
        enemy.image = enemyDeath[enemyDirection][enemyDeathFrame]
        enemyDeathFrame += 1
        schedule(animate_enemy_death, 0.5)
    else:
        enemy.image = enemyDeath[enemyDirection][-1]  
        gameMessage = "you win!"  
        schedule(return_to_menu, 2)  

def return_to_menu():
    global gameMessage
    reset_game() 
    gameMessage = None  

def draw_health_bars():
    max_player_health = 100
    max_enemy_health = 50

    player_bar_width = (playerHealth / max_player_health) * 200
    enemy_bar_width = (enemyHealth / max_enemy_health) * 200

    screen.draw.filled_rect(Rect((10, 10), (player_bar_width, 20)), "green")
    screen.draw.rect(Rect((10, 10), (200, 20)), "white")

    screen.draw.filled_rect(Rect((WIDTH - 210, 10), (enemy_bar_width, 20)), "red")
    screen.draw.rect(Rect((WIDTH - 210, 10), (200, 20)), "white")

    screen.draw.text(f"Player: {playerHealth}/100", (10, 35), fontsize=20, color="white")
    screen.draw.text(f"Enemy: {enemyHealth}/50", (WIDTH - 210, 35), fontsize=20, color="white")

def reset_game():
    global gameState, jumping, jumps, attacking, attackFrame, playerHealth, enemyHealth, playerDead, enemyDead, gameMessage, playerDeathFrame, enemyDeathFrame, enemyAttackFrame, enemyWalkFrame

    gameState = 'menu'
    gameMessage = None  
    player.pos = (50, 440)
    enemy.pos = (800, 500)

    playerHealth, enemyHealth = 100,50
    playerDead, enemyDead, jumping, attacking = False, False, False, False
    attackFrame = 0

    enemy.pos = (800, 500)
    enemyHealth = 50
    enemyDead = False  
    enemyDeathFrame, enemyAttackFrame, enemyWalkFrame = 0, 0, 0
    enemyDirection = "left"
    enemy.image = enemyIdle[enemyDirection][0]

    sounds.background_music.stop()

    gameState = 'play'  
    if sounds_enabled:
        sounds.background_music.play(-1) 

pgzrun.go()