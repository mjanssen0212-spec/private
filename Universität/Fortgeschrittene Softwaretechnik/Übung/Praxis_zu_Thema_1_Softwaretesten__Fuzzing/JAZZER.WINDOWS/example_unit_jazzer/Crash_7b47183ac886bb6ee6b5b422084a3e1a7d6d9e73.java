import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Crash_7b47183ac886bb6ee6b5b422084a3e1a7d6d9e73 {
    static final String base64Bytes = String.join("", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAAFdwQAAAAFdAAQMkJBODdhcXFxcXFxMkJBYXQAEDJCQTg3YXFxcXFxcTJCQWFzcgARamF2YS5sYW5nLkludGVnZXIS4qCk94GHOAIAAUkABXZhbHVleHIAEGphdmEubGFuZy5OdW1iZXKGrJUdC5TgiwIAAHhwAAAAAHNxAH4ABAAAABBxAH4ABng=");

    public static void main(String[] args) throws Throwable {
        Crash_7b47183ac886bb6ee6b5b422084a3e1a7d6d9e73.class.getClassLoader().setDefaultAssertionStatus(true);
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