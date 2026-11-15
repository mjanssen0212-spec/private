package com.example.flappybird;

import java.awt.image.BufferedImage;
import java.util.*;

public class GameSession {
    private final Map<String, Texture> textures;
    private int score;
    private Bird bird;
    private final Highscore highscore = new Highscore();
    private boolean newHighscore;
    private List<Pipe> pipes;
    private int pipeDistTracker;
    private String randomBird;
    private boolean darkTheme;

    private Calendar cal;
    private Random rand;

    public GameSession(Map<String, Texture> textures) {
        rand = new Random();
        this.textures = textures;

        reset();
    }

    public void reset() {
        // Reset game statistics
        score            = 0;
        pipeDistTracker  = 0;
        newHighscore     = false;

        // Get current hour with Calendar
        // If it is past noon, use the dark theme
        cal = Calendar.getInstance();
        int currentHour = cal.get(Calendar.HOUR_OF_DAY);

        // Array of bird colors
        String[] birds = new String[] {
                "yellow",
                "blue",
                "red"
        };

        // Set random scene assets
        darkTheme = currentHour > 12; // If we should use the dark theme
        randomBird = birds[rand.nextInt(3)]; // Random bird color

        // Game bird
        this.bird = new Bird(randomBird, 172, 250, new BufferedImage[] {
                textures.get(randomBird + "Bird1").getImage(),
                textures.get(randomBird + "Bird2").getImage(),
                textures.get(randomBird + "Bird3").getImage()
        });

        // Remove old pipes
        pipes = new ArrayList<Pipe>();
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public Bird getBird() {
        return bird;
    }

    public Highscore getHighscore() {
        return highscore;
    }

    public boolean isNewHighscore() {
        return newHighscore;
    }

    public void setNewHighscore(boolean newHighscore) {
        this.newHighscore = newHighscore;
    }

    public List<Pipe> getPipes() {
        return pipes;
    }

    public void setPipes(List<Pipe> pipes) {
        this.pipes = pipes;
    }

    public int getPipeDistTracker() {
        return pipeDistTracker;
    }

    public void setPipeDistTracker(int pipeDistTracker) {
        this.pipeDistTracker = pipeDistTracker;
    }

    public String getRandomBird() {
        return randomBird;
    }

    public void setRandomBird(String randomBird) {
        this.randomBird = randomBird;
    }

    public boolean isDarkTheme() {
        return darkTheme;
    }

    public void setDarkTheme(boolean darkTheme) {
        this.darkTheme = darkTheme;
    }

    public void reducePipeDist() {
        pipeDistTracker --;
    }

    public void addScore() {
        score++;
    }

    public void addPipe(Pipe pipe) {
        pipes.add(pipe);
    }
}
