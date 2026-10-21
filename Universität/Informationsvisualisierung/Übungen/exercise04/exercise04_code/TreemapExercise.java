package iv.treemap;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.StringJoiner;

public class TreemapExercise extends Application {

    static class Node {
        String name;
        List<Node> children;
        double size;
        double ratio;

        Node(String name, List<Node> children, double size) {
            this.name = name;
            this.children = children != null ? children : new ArrayList<>();
            this.size = size;
            this.ratio = 1.0;
        }

        Node(String name, double size) {
            this(name, null, size);
        }

        Node(String name, List<Node> children) {
            this(name, children, 0);
        }

        @Override
        public String toString() {
            if (children.isEmpty()) {
                return name;
            }
            StringJoiner sj = new StringJoiner(", ");
            for (Node child : children) {
                sj.add(child.toString());
            }
            return name + "(size=" + size + ", ratio=" + ratio + ", children=[" + sj + "])";
        }
    }

    private final List<Color> colors = Arrays.asList(
            Color.web("#e6194b"),
            Color.web("#3cb44b"),
            Color.web("#ffe119"),
            Color.web("#4363d8"),
            Color.web("#f58231"),
            Color.web("#911eb4"),
            Color.web("#46f0f0"),
            Color.web("#f032e6"),
            Color.web("#bcf60c"),
            Color.web("#fabebe"),
            Color.web("#008080")
    );

    private int colorCounter = 0;

    private Color nextColor() {
        Color color = colors.get(colorCounter % colors.size());
        colorCounter++;
        return color;
    }

    private void drawSomething(GraphicsContext gc, double x, double y, double w, double h, String text) {
        Color color = nextColor();
        gc.setFill(color);
        gc.fillRect(x, y, w, h);

        gc.setStroke(Color.WHITE);
        gc.strokeRect(x, y, w, h);

        gc.setFill(Color.WHITE);
        gc.setFont(Font.font("Helvetica", 24));
        gc.fillText(text, x + w / 2 - text.length() * 6, y + h / 2);
    }

    @Override
    public void start(Stage stage) {
        Node tree = new Node("A", Arrays.asList(
                new Node("B", 5),
                new Node("C", Arrays.asList(
                        new Node("D", 2),
                        new Node("E", 3)
                )),
                new Node("F", Arrays.asList(
                        new Node("G", 2),
                        new Node("H", 4),
                        new Node("I", Arrays.asList(
                                new Node("J", 1),
                                new Node("K", 3)
                        ))
                ))
        ));

        double canvasWidth = 600;
        double canvasHeight = 400;

        Canvas canvas = new Canvas(canvasWidth, canvasHeight);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        // Beispiel-Zeichnung
        drawSomething(gc, 20, 10, 200, 60, "Example");
        drawSomething(gc, 50, 90, 400, 60, "Another Example");

        Pane root = new Pane(canvas);
        Scene scene = new Scene(root, canvasWidth, canvasHeight);
        stage.setScene(scene);
        stage.setTitle("Treemap");
        stage.show();

        System.out.println(tree);
    }

    public static void main(String[] args) {
        launch();
    }
}
