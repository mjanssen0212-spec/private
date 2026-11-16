package com.example.flappybird;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;

public class InGameState extends GameStateAbstract{
    private boolean inStartGameState = true;
    private Audio audio;

    public InGameState(Renderer renderer, Ground ground, GameSession gameSession, Audio audio) {
        super(renderer, ground, gameSession);
        this.audio = audio;
    }

    @Override
    public void render(Graphics g) {
        if (inStartGameState) {
            startGameScreen(g);
        }

        PipeManager pm = gameSession.getPipeManager();
        pm.render(renderer, g);
        ground.render(g);
        renderer.drawScore(g, gameSession.getScore(), false, 0, 0);
    }

    @Override
    public GameStateAbstract update() {
        Bird gameBird = gameSession.getBird();
        ground.move();

        if (inStartGameState) {
            return this;
        }
        if (!gameBird.isAlive()) {
            nextGameState.onEnter();
            return nextGameState;
        }

        updatePipes();
        gameBird.inGame();
        if (!gameBird.isAlive()) {
            audio.hit();
        }
        return this;

    }

    private void updatePipes() {
        PipeManager pm = gameSession.getPipeManager();
        Bird gameBird = gameSession.getBird();
        Rectangle hitbox = gameBird.getHitbox();

        //Update all Pipes
        pm.update();

        if (pm.collide(hitbox)) {
            // Kill bird
            gameBird.kill();

            return;
        }

        if (pm.collectPoints(hitbox)) {
            audio.point();
            gameSession.addScore();
        }
    }

    @Override
    public GameStateAbstract handleKeyEvent(KeyEvent e) {
        int keycode = e.getKeyCode();

        if(keycode == KeyEvent.VK_SPACE) {
            inStartGameState = false;
            flap();
        }

        return this;
    }

    @Override
    public GameStateAbstract handleMouseEvent(MouseEvent e) {
        inStartGameState = false;
        flap();

        return this;
    }

    @Override
    public void onEnter() {
        inStartGameState = true;
        gameSession.getBird().setGameStartPos();
    }

    public void startGameScreen (Graphics g) {
        // Get ready text
        renderer.drawComponent("getReadyText", g);

        // Instructions image
        renderer.drawComponent("instructions", g);
    }



    private void flap() {
        gameSession.getBird().jump();
        audio.jump();
    }
}
