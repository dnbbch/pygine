import pygine as pg
import pygame

pygame.init()

WIDTH, HEIGHT = 1200, 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("All Animations Demo")
clock = pygame.time.Clock()

stance_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
stance_sprite.add_animation("stance", [0, 1, 2, 3], fps=8, loop=True)
stance_sprite.play_animation("stance")
stance_sprite.set_position(150, 150)

run_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
run_sprite.add_animation("run", [4, 5, 6, 7, 8, 9, 10, 11], fps=8, loop=True)
run_sprite.play_animation("run")
run_sprite.set_position(450, 150)

swing_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
swing_sprite.add_animation("swing", [12, 13, 14, 15], fps=8, loop=True)
swing_sprite.play_animation("swing")
swing_sprite.set_position(750, 150)

block_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
block_sprite.add_animation("block", [16, 17], fps=8, loop=True)
block_sprite.play_animation("block")
block_sprite.set_position(1050, 150)

hit_die_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
hit_die_sprite.add_animation("hit_die", [18, 19, 20, 21, 22, 23], fps=8, loop=True)
hit_die_sprite.play_animation("hit_die")
hit_die_sprite.set_position(150, 400)

cast_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
cast_sprite.add_animation("cast", [24, 25, 26, 27], fps=8, loop=True)
cast_sprite.play_animation("cast")
cast_sprite.set_position(450, 400)

shoot_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
shoot_sprite.add_animation("shoot", [28, 29, 30, 31], fps=8, loop=True)
shoot_sprite.play_animation("shoot")
shoot_sprite.set_position(750, 400)

walk_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
walk_sprite.add_animation("walk", [32, 33, 34, 35, 36, 37, 38, 39], fps=8, loop=True)
walk_sprite.play_animation("walk")
walk_sprite.set_position(1050, 400)

duck_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
duck_sprite.add_animation("duck", [40, 41], fps=8, loop=True)
duck_sprite.play_animation("duck")
duck_sprite.set_position(150, 650)

jump_fall_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
jump_fall_sprite.add_animation("jump_fall", [42, 43, 44, 45, 46, 47], fps=8, loop=True)
jump_fall_sprite.play_animation("jump_fall")
jump_fall_sprite.set_position(450, 650)

ascend_sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
ascend_sprite.add_animation("stand", [64], fps=8, loop=True)
ascend_sprite.play_animation("stand")
ascend_sprite.set_position(750, 650)

text1 = pg.Text(120, 200, "Stance", size=24)
text2 = pg.Text(430, 200, "Run", size=24)
text3 = pg.Text(720, 200, "Swing", size=24)
text4 = pg.Text(1020, 200, "Block", size=24)
text5 = pg.Text(110, 450, "Hit/Die", size=24)
text6 = pg.Text(430, 450, "Cast", size=24)
text7 = pg.Text(720, 450, "Shoot", size=24)
text8 = pg.Text(1020, 450, "Walk", size=24)
text9 = pg.Text(120, 700, "Duck", size=24)
text10 = pg.Text(400, 700, "Jump/Fall", size=24)
text11 = pg.Text(720, 700, "Stand", size=24)

running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    stance_sprite.update(dt)
    run_sprite.update(dt)
    swing_sprite.update(dt)
    block_sprite.update(dt)
    hit_die_sprite.update(dt)
    cast_sprite.update(dt)
    shoot_sprite.update(dt)
    walk_sprite.update(dt)
    duck_sprite.update(dt)
    jump_fall_sprite.update(dt)
    ascend_sprite.update(dt)
    
    window.fill((40, 40, 80))
    
    window.blit(stance_sprite.image, stance_sprite.rect)
    window.blit(run_sprite.image, run_sprite.rect)
    window.blit(swing_sprite.image, swing_sprite.rect)
    window.blit(block_sprite.image, block_sprite.rect)
    window.blit(hit_die_sprite.image, hit_die_sprite.rect)
    window.blit(cast_sprite.image, cast_sprite.rect)
    window.blit(shoot_sprite.image, shoot_sprite.rect)
    window.blit(walk_sprite.image, walk_sprite.rect)
    window.blit(duck_sprite.image, duck_sprite.rect)
    window.blit(jump_fall_sprite.image, jump_fall_sprite.rect)
    window.blit(ascend_sprite.image, ascend_sprite.rect)
    
    text1.draw(window)
    text2.draw(window)
    text3.draw(window)
    text4.draw(window)
    text5.draw(window)
    text6.draw(window)
    text7.draw(window)
    text8.draw(window)
    text9.draw(window)
    text10.draw(window)
    text11.draw(window)
    
    pygame.display.update()

pygame.quit()
