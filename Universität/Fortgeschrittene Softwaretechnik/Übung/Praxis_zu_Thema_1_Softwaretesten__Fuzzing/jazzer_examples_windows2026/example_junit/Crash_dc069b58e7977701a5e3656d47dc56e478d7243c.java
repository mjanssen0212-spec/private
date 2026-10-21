import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Crash_dc069b58e7977701a5e3656d47dc56e478d7243c {
    static final String base64Bytes = String.join("", "rO0ABXNyABNqYXZhLnV0aWwuQXJyYXlMaXN0eIHSHZnHYZ0DAAFJAARzaXpleHAAAAAFdwQAAAAFdABkYDFAMDdgYDFAMFFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUVFRUXQAGWAxQDA3YGAxQDBRUVFRUVFRUVFRUVFRUVFzcgARamF2YS5sYW5nLkludGVnZXIS4qCk94GHOAIAAUkABXZhbHVleHIAEGphdmEubGFuZy5OdW1iZXKGrJUdC5TgiwIAAHhwAAAAAHNxAH4ABAAAABlxAH4ABng=");

    public static void main(String[] args) throws Throwable {
        Crash_dc069b58e7977701a5e3656d47dc56e478d7243c.class.getClassLoader().setDefaultAssertionStatus(true);
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