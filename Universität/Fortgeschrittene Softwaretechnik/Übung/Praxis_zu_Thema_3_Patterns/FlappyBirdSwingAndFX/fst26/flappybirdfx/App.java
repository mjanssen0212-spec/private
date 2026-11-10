package fst26.flappybirdfx;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

// Original Version: https://github.com/ImKennyYip/flappy-bird-java
// ported to JavaFX

public class App extends Application {

    @Override
    public void start(Stage stage) {
        FlappyBird flappyBird = new FlappyBird();

        StackPane root = new StackPane(flappyBird);
        Scene scene = new Scene(root, flappyBird.getWidth(), flappyBird.getHeight());
        scene.setOnKeyPressed(flappyBird::keyPressed);

        stage.setTitle("Flappy Bird");
        stage.setScene(scene);
        stage.setResizable(false);
        stage.centerOnScreen();
        stage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
