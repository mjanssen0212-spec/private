package com.example.flappybird;

import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.event.MouseEvent;

public class GameOverState extends GameStateAbstract {
    private String medal;

    public GameOverState(Renderer renderer, Ground ground, GameSession gameSession) {
        super(renderer, ground, gameSession);
    }

    @Override
    public void render(Graphics g) {
        ground.render(g);
        gameOver(g);
    }

    @Override
    public GameStateAbstract update() {
        return this;
    }

    @Override
    public GameStateAbstract handleKeyEvent(KeyEvent e) {
        int keycode = e.getKeyCode();

        if (keycode == KeyEvent.VK_ENTER) {
            nextGameState.onEnter();
            gameSession.reset();
            return nextGameState;
        }

        return this;
    }

    @Override
    public GameStateAbstract handleMouseEvent(MouseEvent e) {
        Point clickedPoint = e.getPoint();

        if(isTouching(renderer.getTextureRect("playButton"), clickedPoint)) {
            gameSession.reset();
            nextGameState.onEnter();
            return nextGameState;
        } else if (isTouching(renderer.getTextureRect("leaderboard"), clickedPoint)) {
            showErrorMessage();
            return this;
        }
        return this;
    }

    @Override
    public void onEnter() {
        int score = gameSession.getScore();
        Highscore highscore = gameSession.getHighscore();

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

        // Only award a medal if they deserve it
        if (score > 9) {
            renderer.drawComponent(medal, g);
        }

        // Buttons
        renderer.drawComponent("playButton", g);
        renderer.drawComponent("leaderboard", g);

    }
}
