package cg.ueb;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

public class Template extends Application {

    // Colors for the bars
    private String[] colors = {"red", "yellow", "pink", "brown", "purple"};
    private int scale = 10;

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Draw Pixels with JavaFX");

        // Create a canvas
        Canvas canvas = new Canvas(500, 400);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        drawPixel(gc, 8, 8, colors[0]);
        drawPixel(gc, 9, 9, colors[0]);
        drawPixel(gc, 10, 10, colors[0]);
        drawPixel(gc, 11, 10, colors[1]);
        drawPixel(gc, 12, 10, colors[1]);

        StackPane root = new StackPane();
        root.getChildren().add(canvas);
        primaryStage.setScene(new Scene(root));
        primaryStage.show();
    }

    private void drawPixel(GraphicsContext gc, int x, int y, String color) {
        gc.setFill(Color.web(color));
        gc.fillRect(x * scale, y * scale, scale, scale);
    }

    public static void main(String[] args) {
        launch(args);
    }
}
