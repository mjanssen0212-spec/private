package com.example.flappybird;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;
import java.util.ArrayList;

public class GameOverState extends GameStateAbstract {
    private Renderer renderer;
    private Ground ground;
    private GameSession gameSession;
    private String medal;
    private GameStateAbstract nextGameState;
    private Audio audio = new Audio();

    public GameOverState(Renderer renderer, Ground ground, GameSession gameSession) {
        this.renderer = renderer;
        this.ground = ground;
        this.gameSession = gameSession;
    }

    @Override
    public void render(Graphics g) {
        ground.render(g);
        gameOver(g);
    }

    @Override
    public GameStateAbstract update(Graphics g) {
        return this;
    }

    @Override
    public GameStateAbstract handleKeyEvent(KeyEvent e) {
        int keycode = e.getKeyCode();

        if (keycode == KeyEvent.VK_ENTER) {
            return nextGameState;
        }

        return this;
    }

    @Override
    public GameStateAbstract handleMouseEvent(MouseEvent e) {
        Point clickedPoint = e.getPoint();

        if(isTouching(renderer.getTextureRect("playButton"), clickedPoint)) {
            gameSession.reset();
            return nextGameState;
        } else if (isTouching(renderer.getTextureRect("leaderboard"), clickedPoint)) {
            return this;
        }
        return this;
    }

    @Override
    public void updatePipes(Graphics g) {

    }


    public void setNextGameState(GameStateAbstract nextGameState) {
        this.nextGameState = nextGameState;
    }

    public void gameOver (Graphics g) {

        int score = gameSession.getScore();
        Highscore highscore = gameSession.getHighscore();
        // Game over text
        renderer.drawComponent("gameOverText", g);

        // Scorecard
        renderer.drawComponent("scoreCard", g);

        // New highscore image
        if (gameSession.isNewHighscore()) {
            renderer.drawComponent("newHighscore", g);
        }

        // Draw mini fonts for current and best scores
        renderer.drawScore(g, score, true, 303, 276);
        renderer.drawScore(g, highscore.bestScore(), true, 303, 330);

        // Handle highscore
        if (score > highscore.bestScore()) {

            // New best score
            gameSession.setNewHighscore(true);
            highscore.setNewBest(score); // Set in data file
        }

        // Medal
        if (score >= 10) { medal = "bronze"; }
        if (score >= 20) { medal = "silver"; }
        if (score >= 30) { medal = "gold"; }
        if (score >= 40) { medal = "platinum"; }

        // Only award a medal if they deserve it
        if (score > 9) {
            renderer.drawComponent(medal, g);
        }

        // Buttons
        renderer.drawComponent("playButton", g);
        renderer.drawComponent("leaderboard", g);

    }
}
