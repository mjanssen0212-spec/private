
@rem set CLASSPATH=.\;%JAVA_HOME%\lib;..\jazzer_standalone.jar;.\hamcrest-core-1.3.jar;.\junit-4.13.2.jar

@rem set CLASSPATH=.\;%JAVA_HOME%\lib;..\jazzer_standalone.jar;.\hamcrest-core-1.3.jar;..\jazzer-junit-0.30.0.jar;..\junit-jupiter-6.1.3.jar;..\junit-jupiter-api-6.1.3.jar;..\junit-jupiter-engine-6.1.3.jar;..\apiguardian-api-1.1.2.jar

set CLASSPATH=.;%JAVA_HOME%\lib;.\lib\jazzer_standalone.jar;.\lib\*


javac ExampleMatcher.java

java  ExampleMatcher blabla

java  ExampleMatcher 7a7a7a7a7a7a7a7a

javac EmailMatcherFuzzTest.java

java EmailMatcherFuzzTest

java -cp %CLASSPATH% com.code_intelligence.jazzer.Jazzer --target_class=EmailMatcherFuzzTest


@rem java org.junit.runner.JUnitCore MagicStringsTest

@rem java -jar ..\jazzer_standalone.jar --cp=%CLASSPATH% --target_class=MagicStringsFuzzTest
@rem java -cp <classpath>;<path/to/jazzer.jar>;<path/to/jazzer-junit.jar> com.code_intelligence.jazzer.Jazzer --target_class=<fuzz-test-class> [args...]

@rem ./jazzer --cp=<classpath> --target_class=<fuzz test class>

@rem Alternativ Klassenpfad im Befehl angeben:

@rem javac -cp .\;%JAVA_HOME%\lib Example.java

@rem java -cp .\;%JAVA_HOME%\lib Example blabla

@rem javac -cp .\;%JAVA_HOME%\lib;.\hamcrest-core-1.3.jar;.\junit-4.13.2.jar MagicStringsTest.java

@rem java -cp .\;%JAVA_HOME%\lib;.\hamcrest-core-1.3.jar;.\junit-4.13.2.jar org.junit.runner.JUnitCore MagicStringsTest

