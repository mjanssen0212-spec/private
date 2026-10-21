import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Crash_a4abc52082870eb83b55d7370cf8b81964b5d915 {
    static final String base64Bytes = String.join("", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAAFdwQAAAAFdABjNzc3NzdYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFgxODU1NzYwMTIxdABjNzc3NzdYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFhYWFgxODU1NzYwMTIxc3IAEWphdmEubGFuZy5JbnRlZ2VyEuKgpPeBhzgCAAFJAAV2YWx1ZXhyABBqYXZhLmxhbmcuTnVtYmVyhqyVHQuU4IsCAAB4cAAAAABzcQB+AAQAAAAZcQB+AAZ4");

    public static void main(String[] args) throws Throwable {
        Crash_a4abc52082870eb83b55d7370cf8b81964b5d915.class.getClassLoader().setDefaultAssertionStatus(true);
        try {
            Method fuzzerInitialize = MagicStringsFuzzTest.class.getMethod("fuzzerInitialize");
            fuzzerInitialize.invoke(null);
        } catch (NoSuchMethodException ignored) {
            try {
                Method fuzzerInitialize = MagicStringsFuzzTest.class.getMethod("fuzzerInitialize", String[].class);
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
        MagicStringsFuzzTest.fuzzerTestOneInput(input);
    }
}