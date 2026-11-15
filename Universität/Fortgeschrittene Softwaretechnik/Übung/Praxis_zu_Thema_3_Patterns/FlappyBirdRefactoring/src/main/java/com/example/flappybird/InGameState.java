package com.example.flappybird;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.util.ArrayList;

public class InGameState extends GameStateAbstract{
    private Renderer renderer;
    private Ground ground;
    private GameSession gameSession;
    private GameStateAbstract nextGameState;
    private boolean inStartGameState = true;
    private Audio audio = new Audio();

    public InGameState(Renderer renderer, Ground ground, GameSession gameSession) {
        this.renderer = renderer;
        this.ground = ground;
        this.gameSession = gameSession;
    }

    @Override
    public void render(Graphics g) {
        if (inStartGameState) {
            startGameScreen(g);
//            inStartGameState = false;
        } else {
            updatePipes(g);
            gameSession.getBird().inGame();
        }

        ground.render(g);
        renderer.drawScore(g, gameSession.getScore(), false, 0, 0);
    }

    @Override
    public GameStateAbstract update(Graphics g) {
        if (inStartGameState) {
            return this;
        }
        if (!gameSession.getBird().isAlive()) {
            return nextGameState;
        }

        updatePipes(g);
        return this;

    }

    @Override
    public void updatePipes(Graphics g) {
        int pipeDist = gameSession.getPipeDistTracker();
        Bird gameBird = gameSession.getBird();
        ArrayList<Pipe> pipes = (ArrayList<Pipe>) gameSession.getPipes();

        // Decrease distance between pipes
        gameSession.reducePipeDist();


        // Initialize pipes as null
        Pipe topPipe = null;
        Pipe bottomPipe = null;

        // If there is no distance,
        // a new pipe is needed
        if (pipeDist < 0) {

            // Reset distance
            gameSession.setPipeDistTracker(Pipe.PIPE_DISTANCE);

            for (Pipe p : pipes) {

                // If pipe is out of screen
                if (p.getX() < 0) {
                    if (topPipe == null) {
                        topPipe = p;
                    }
                    else if (bottomPipe == null) {
                        bottomPipe = p;
                    }
                    topPipe.setCanAwardPoint(true);
                }
            }

            // Move and handle initial creation of top and bottom pipes

            topPipe = addOrReset(topPipe, "top");

            bottomPipe = addOrReset(bottomPipe, "bottom");
            bottomPipe.setCanAwardPoint(false);

            // Set y-coordinate of bottom pipe based on
            // y-coordinate of top pipe
            bottomPipe.setY(topPipe.getY() + Pipe.PIPE_SPACING);

        }

        // Move and draw each pipe

        for (Pipe p : pipes) {

            // Move the pipe
            p.move();

            // Draw the top and bottom pipes
            renderer.drawComponent(p.getY() <= 0 ? "pipe-top" : "pipe-bottom", p.getX(), p.getY(), g);

            // Check if bird hits pipes
            if (p.collide(
                    gameBird.getHitbox()
            )) {
                // Kill bird and play sound
                gameBird.kill();
                audio.hit();
            } else {

                // Checks if bird passes a pipe
                if (gameBird.getX() >= p.getX() + p.WIDTH / 2) {

                    // Increase score and play sound
                    if (p.getCanAwardPoint()) {
                        audio.point();
                        gameSession.addScore();
                        p.setCanAwardPoint(false);
                    }
                }
            }
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

    public void setNextGameState(GameStateAbstract nextGameState) {
        this.nextGameState = nextGameState;
    }

    public void startGameScreen (Graphics g) {

        // Set bird's new position
        gameSession.getBird().setGameStartPos();

        // Get ready text
        renderer.drawComponent("getReadyText", g);

        // Instructions image
        renderer.drawComponent("instructions", g);

    }

    private Pipe addOrReset(Pipe p, String pipeType) {
        if (p == null) {
            p = new Pipe(pipeType);
            gameSession.addPipe(p);
        } else {
            p.reset();
        }

        return p;
    }

    private void flap() {
        gameSession.getBird().jump();
        audio.jump();
    }
}
