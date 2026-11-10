package fst26.flappybirdfx;

import java.util.ArrayList;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.image.Image;
import javafx.scene.input.KeyCode;
import javafx.scene.input.KeyEvent;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.util.Duration;

// Original Version: https://github.com/ImKennyYip/flappy-bird-java
// ported to JavaFX

public class FlappyBird extends Canvas {
    int boardWidth = 360;
    int boardHeight = 640;

    //images
    Image backgroundImg;
    Image birdImg;
    Image topPipeImg;
    Image bottomPipeImg;

    //bird class
    int birdX = boardWidth / 8;
    int birdY = boardHeight / 2;
    int birdWidth = 34;
    int birdHeight = 24;

    class Bird {
        int x = birdX;
        int y = birdY;
        int width = birdWidth;
        int height = birdHeight;
        Image img;

        Bird(Image img) {
            this.img = img;
        }
    }

    //pipe class
    int pipeX = boardWidth;
    int pipeY = 0;
    int pipeWidth = 64;  //scaled by 1/6
    int pipeHeight = 512;

    class Pipe {
        int x = pipeX;
        int y = pipeY;
        int width = pipeWidth;
        int height = pipeHeight;
        Image img;
        boolean passed = false;

        Pipe(Image img) {
            this.img = img;
        }
    }

    //game logic
    Bird bird;
    int velocityX = -4; //move pipes to the left speed (simulates bird moving right)
    int velocityY = 0;  //move bird up/down speed.
    int gravity = 1;

    ArrayList<Pipe> pipes;

    Timeline gameLoop;
    Timeline placePipeTimer;
    boolean gameOver = false;
    double score = 0;

    FlappyBird() {
        setWidth(boardWidth);
        setHeight(boardHeight);

        //load images
        backgroundImg = new Image(getClass().getResourceAsStream("flappybirdbg.png"));
        birdImg = new Image(getClass().getResourceAsStream("flappybird.png"));
        topPipeImg = new Image(getClass().getResourceAsStream("toppipe.png"));
        bottomPipeImg = new Image(getClass().getResourceAsStream("bottompipe.png"));

        //bird
        bird = new Bird(birdImg);
        pipes = new ArrayList<Pipe>();

        //place pipes timer
        placePipeTimer = new Timeline(new KeyFrame(Duration.millis(1500), e -> placePipes()));
        placePipeTimer.setCycleCount(Timeline.INDEFINITE);
        placePipeTimer.play();

        //game timer
        gameLoop = new Timeline(new KeyFrame(Duration.millis(1000.0 / 60), e -> update()));
        gameLoop.setCycleCount(Timeline.INDEFINITE);
        gameLoop.play();

        draw();
    }

    void placePipes() {
        //(0-1) * pipeHeight/2.
        // 0 -> -128 (pipeHeight/4)
        // 1 -> -128 - 256 (pipeHeight/4 - pipeHeight/2) = -3/4 pipeHeight
        int randomPipeY = (int) (pipeY - pipeHeight / 4 - Math.random() * (pipeHeight / 2));
        int openingSpace = boardHeight / 4;

        Pipe topPipe = new Pipe(topPipeImg);
        topPipe.y = randomPipeY;
        pipes.add(topPipe);

        Pipe bottomPipe = new Pipe(bottomPipeImg);
        bottomPipe.y = topPipe.y + pipeHeight + openingSpace;
        pipes.add(bottomPipe);
    }

    void draw() {
        GraphicsContext g = getGraphicsContext2D();

        //background
        g.drawImage(backgroundImg, 0, 0, boardWidth, boardHeight);

        //bird
        g.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);

        //pipes
        for (int i = 0; i < pipes.size(); i++) {
            Pipe pipe = pipes.get(i);
            g.drawImage(pipe.img, pipe.x, pipe.y, pipe.width, pipe.height);
        }

        //score
        g.setFill(Color.WHITE);
        g.setFont(Font.font("Arial", 32));
        if (gameOver) {
            g.fillText("Game Over: " + (int) score, 10, 35);
        } else {
            g.fillText(String.valueOf((int) score), 10, 35);
        }
    }

    void move() {
        //bird
        velocityY += gravity;
        bird.y += velocityY;
        bird.y = Math.max(bird.y, 0); //apply gravity to current bird.y, limit the bird.y to top of the canvas

        //pipes
        for (int i = 0; i < pipes.size(); i++) {
            Pipe pipe = pipes.get(i);
            pipe.x += velocityX;

            if (!pipe.passed && bird.x > pipe.x + pipe.width) {
                score += 0.5; //0.5 because there are 2 pipes! so 0.5*2 = 1, 1 for each set of pipes
                pipe.passed = true;
            }

            if (collision(bird, pipe)) {
                gameOver = true;
            }
        }

        if (bird.y > boardHeight) {
            gameOver = true;
        }
    }

    boolean collision(Bird a, Pipe b) {
        return a.x < b.x + b.width &&   //a's top left corner doesn't reach b's top right corner
               a.x + a.width > b.x &&   //a's top right corner passes b's top left corner
               a.y < b.y + b.height &&  //a's top left corner doesn't reach b's bottom left corner
               a.y + a.height > b.y;    //a's bottom left corner passes b's top left corner
    }

    //called every ~16 ms by the gameLoop timeline
    void update() {
        move();
        draw();
        if (gameOver) {
            placePipeTimer.stop();
            gameLoop.stop();
        }
    }

    public void keyPressed(KeyEvent e) {
        if (e.getCode() == KeyCode.SPACE) {
            velocityY = -9;

            if (gameOver) {
                //restart game by resetting conditions
                bird.y = birdY;
                velocityY = 0;
                pipes.clear();
                gameOver = false;
                score = 0;
                gameLoop.play();
                placePipeTimer.play();
            }
        }
    }
}
