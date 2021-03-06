# -*- coding: utf-8 -*-
#!/usr/bin/python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
#est
class PongBall(Widget):
    
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
   
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongPaddle(Widget):
    
    score = NumericProperty(0)
    
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            tmp = self.center_y
            self.height *= 0.9
            self.center_y = tmp
            vel = bounced * 1.2
            ball.velocity = vel.x,vel.y + offset
            


class PongGame(Widget):

    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)    
    

    def serve_ball(self, vel = Vector(4, 0).rotate(randint(0,360))):
        self.ball.center = self.center
        self.ball.velocity = vel

    def reset_paddles(self):
        self.player1.height = self.player2.height = 200 
        self.player1.center_y = self.player2.center_y = self.center_y

    def update(self, dt):
        
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
            
        if self.ball.x < self.x:
            self.player2.score += 1
            self.reset_paddles()
            self.serve_ball(Vector(4, 0))
    
        if self.ball.right > self.width:
            self.player1.score += 1
            self.reset_paddles()
            self.serve_ball(Vector(-4, 0))
        
        self.ball.move()
    def on_touch_move(self,touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
    
if __name__ == '__main__':
    PongApp().run()
