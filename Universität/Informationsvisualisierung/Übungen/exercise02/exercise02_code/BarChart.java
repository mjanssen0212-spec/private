package iv.charts;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.stage.Stage;

import java.util.LinkedHashMap;
import java.util.Map;

public class BarChart extends Application {

    // Sample data for the bar chart
    private final Map<String, Integer> data = new LinkedHashMap<>() {{
        put("Apples", 30);
        put("Bananas", 15);
        put("Cherries", 25);
        put("Dates", 10);
        put("Elderberries", 20);
    }};

    private final Color[] colors = {
            Color.RED, Color.GOLD, Color.HOTPINK, Color.SADDLEBROWN, Color.PURPLE
    };

    @Override
    public void start(Stage primaryStage) {
        int canvasWidth = 500;
        int canvasHeight = 400;
        int padding = 40;

        Canvas canvas = new Canvas(canvasWidth, canvasHeight);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        drawBarChart(gc, canvasWidth, canvasHeight, padding);

        Scene scene = new Scene(new javafx.scene.Group(canvas));
        primaryStage.setTitle("Simple Bar Chart with JavaFX");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    private void drawBarChart(GraphicsContext gc, int width, int height, int padding) {
        double maxValue = data.values().stream().mapToDouble(i -> i).max().orElse(1);
        int numBars = data.size();
        double barWidth = (width - 2 * padding) / numBars;

        int index = 0;
        for (Map.Entry<String, Integer> entry : data.entrySet()) {
            String label = entry.getKey();
            double value = entry.getValue();
            double barHeight = (value / maxValue) * (height - 2 * padding);

            double x0 = padding + index * barWidth;
            double y0 = height - padding - barHeight;
            double x1 = x0 + barWidth * 0.8;
            double y1 = height - padding;

            // Draw bar
            gc.setFill(colors[index % colors.length]);
            gc.fillRect(x0, y0, x1 - x0, y1 - y0);
            gc.setStroke(Color.BLACK);
            gc.strokeRect(x0, y0, x1 - x0, y1 - y0);

            // Value label above bar
            gc.setFill(Color.BLACK);
            gc.setFont(new Font(12));
            gc.fillText(String.valueOf((int) value), (x0 + x1) / 2 - 10, y0 - 5);

            // Category label below bar
            gc.fillText(label, (x0 + x1) / 2 - 20, y1 + 15);

            index++;
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}

