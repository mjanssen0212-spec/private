import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Crash_0c1791fda689001e383e01e24b7dffc0a4b372d4 {
    static final String base64Bytes = String.join("", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAABdwQAAAABdAAfbWFnaWNzdHJpbmc0bWdpYWNzdHJobmc0YUNzdHJobng=");

    public static void main(String[] args) throws Throwable {
        Crash_0c1791fda689001e383e01e24b7dffc0a4b372d4.class.getClassLoader().setDefaultAssertionStatus(true);
        try {
            Method fuzzerInitialize = ExampleFuzzer.class.getMethod("fuzzerInitialize");
            fuzzerInitialize.invoke(null);
        } catch (NoSuchMethodException ignored) {
            try {
                Method fuzzerInitialize = ExampleFuzzer.class.getMethod("fuzzerInitialize", String[].class);
                fuzzerInitialize.invoke(null, (Object) args);
            } catch (NoSuchMethodException ignored1) {
            } catch (IllegalAccessException | InvocationTargetException e) {
                e.printStackTrace();
                System.exit(1);
            }
        } catch (IllegalAccessException | InvocationTargetException e) {
            e.printStackTrace();
            System.exit(1);
        }
        com.code_intelligence.jazzer.api.CannedFuzzedDataProvider input = new com.code_intelligence.jazzer.api.CannedFuzzedDataProvider(base64Bytes);
        ExampleFuzzer.fuzzerTestOneInput(input);
    }
}