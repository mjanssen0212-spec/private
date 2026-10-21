
set CLASSPATH=".;%JAVA_HOME%\lib;..\lib\jazzer_standalone.jar;..\lib"

javac ExampleFuzzer.java

javac ExampleFuzzerHooks.java

java  com.code_intelligence.jazzer.Jazzer --target_class=ExampleFuzzer --custom_hooks=ExampleFuzzerHooks

@rem java  com.code_intelligence.jazzer.Jazzer --target_class=ExampleFuzzer 

@rem Mit Klassenpfad im Befehl:
@rem javac -cp .\;%JAVA_HOME%\lib;.\jazzer_standalone.jar ExampleFuzzer.java
@rem javac -cp .\;%JAVA_HOME%\lib;.\jazzer_standalone.jar ExampleFuzzerHooks.java
@rem java -cp .\;%JAVA_HOME%\lib;.\jazzer_standalone.jar com.code_intelligence.jazzer.Jazzer --target_class=ExampleFuzzer --custom_hooks=ExampleFuzzerHooks



@rem JAZZER als Anwendung 
@rem in UNIX
@rem ./jazzer --cp=<classpath> --target_class=<fuzz test class>

@rem in WINDOWS
@rem .\jazzer.exe --cp=%JAVA_HOME%\lib;.\jazzer_standalone.jar --target_class=ExampleFuzzer

@rem MIT -jar funktioniert nicht
@rem java -cp ".\*" -jar jazzer_standalone.jar  --cp=".\*;jazzer_standalone.jar;%JAVA_HOME%\lib\*" --target_class=ExampleFuzzer

@rem java -cp .\;%JAVA_HOME%\lib;.\jazzer_standalone.jar com.code_intelligence.jazzer.Jazzer --target_class=ExampleFuzzer


