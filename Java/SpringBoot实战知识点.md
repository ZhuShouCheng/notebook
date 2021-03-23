

### SpringBoot实战知识点

#### SpringApplication

[SpringApplication](https://docs.spring.io/spring-boot/docs/current/reference/html/boot-features-spring-application.html)类用于引导和启动一个Spring应用程序(即SpringBoot开发的应用)。通常用SpringBoot开发一个应用程序时，在主类的main函数中可以通过如下代码启动一个Spring应用：

```Java
@SpringBootApplication
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
}
```

静态方法`run(Class<?> primarySource, String... args))`第一个参数接受一个Spring容器配置类。

SpringApplication类会做如下事情启动应用：

- 为应用创建一个合适的ApplicationContext
- 注册一个CommandLinePropertySource，通过CommandLinePropertySource可以对外暴露命令行参数，并将命令行参数与spring应用中用到的properties关联起来
- 启动ApplicationContext
- 执行所有的CommandLineRunner类型bean

在SpringApplication的构造函数中，主要完成下列初始化工作

- 初始化Spring容器的配置类**primarySources**
- 推断应用程序的类型，进而根据应用程序的类型创建恰当的ApplicationContext
- 初始化指定的**ApplicationContextInitializer**列表
- 初始化指定的**ApplicationListener**列表
- 推断main class的类名称

ApplicationContext的应用类型只有三种 1.非web类应用 2.Servlet类型的web应用 3.reactive类型的web应用
初始化ApplicationContextInitializer&ApplicationListener借助SpringFactoriesLoader完成，主要通过读取META-INF/spring.factories文件中的配置

run方法的执行逻辑：

- 创建StopWatch对象，用于统计应用的启动时间
- 加载SpringApplicationRunListener
- 创建并配置Environment
- 创建对应类型的ApplicationContext，将之前创建好的Environment设置给创建好的ApplicationContext
- 完成ApplicationContext的初始化
- 向ApplicationContext中加载所有的bean

参考：[深入理解SpringApplication](https://segmentfault.com/a/1190000019560001)



#### 注解

`@SpringBootApplication`

该注解包含三个注解`@ComponentScan`、`@EnableAutoConfiguration`,`@SpringBootConfiguration`，与三者等价

`@ComponentScan`

该注解默认会扫描该类所在的包下所有的配置类

`@EnableAutoConfiguration`

该注解表示自动装载bean

`@SpringBootConfiguration`

该注解的作用与`@Configuration`作用相同，都是用来声明当前类是一个配置类

`@Controller`

该注解表明标记的类是一个SpringMvc Controller对象，和`@RequestMapping`配合用来处理http请求。视图解析器将解析return 的jsp,html页面，并且跳转到相应页面，若返回json等内容到页面，则需要加`@ResponseBody`注解

`@RestController`

相当于`@Controller`+`@ResponseBody`两个注解的结合，视图解析器将返回json数据，但无法解析jsp，html\

`@RequestBody`

主要用来接收前端传递给后端的json字符串中的数据的(请求体中的数据的) 

`@GetMapping`

该注解用于处理请求方法的GET类型，通过内部调用注解`@RequestMapping`实现

------------------------

`@Data`

使用该注解需先引用lombok类库

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
```

该注解用来标记实体类，将自动生成get、set、toString方法

`@Component`

该注解用于将pojo对象注入到spring容器中

`@Value`

该注解用于将外部值动态注入到Bean中   

1. `@Value("${}")`用于从配置文件中传值

2. `@Value("#{}")`用于SpEL表达式

`@ConfigurationProperties(prefix="")`

该注解用于指明配置文件注入信息的前缀

`@Autowired`

该注解可以对成员变量、方法和构造函数进行标注，来完成自动装配的工作

--------------------

`@EnableAdminServer`

该注解用于导入Spring Boot Admin Server配置

`@Slf4j`

添加该注解后，可直接使用log来打印日志

------

Lombok

Lombok 是一种 Java™ 实用工具，可用来帮助开发人员消除 Java 的冗长，尤其是对于简单的 Java 对象（POJO）。它通过注解实现这一目的。

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
</dependency>
```

`@Data` 自动生成get set tostring equal等方法
`@Builder` 可以使用builder方法构造
`@NoArgsConstructor` 自动生成无参构造器
`@AllArgsConstructor` 自动生成有参构造器

`@RequestBody`

该注解用来将Java对象转为json格式的数据。

-----

`@ControllerAdvice`

该注解实现三个功能

1. 全局异常处理(配合`@ExceptionHandler`使用)
2. 全局数据绑定
3. 全局数据预处理

`@EqualsAndHashCode(callSuper = true)`

使用该注解标注后，将父类属性也进行比较

`@Aspect`

------

`@PathVariable("xxx")`
通过 @PathVariable 可以将URL中占位符参数{xxx}绑定到处理器类的方法形参中@PathVariable(“xxx“) 

`@Repository`

@Repository和@Controller、@Service、@Component的作用差不多，都是把对象交给spring管理。@Repository用在持久层DAO的接口上，这个注解是将接口的一个实现类交给spring管理。该注解的作用不只是将类识别为Bean，同时它还能将所标注的类中抛出的数据访问异常封装为 Spring 的数据访问异常类型。


#### 配置文件

配置文件的作用：修改SpringBoot自动配置的默认值

SpringBoot使用一个全局的配置文件，配置文件名是固定的；

- application.properties
- application.yml

##### application.yml

YAML（YAML Ain't Markup Language）

以数据为中心

```yaml
server:
  port: 8080
  servlet:
    context-path: /demo
spring:
  profiles:
    active: dev
```

多配置文件时，文件名必须为 application-{profile}.properties/yml

在application.yml中使用spring.profiles.active=xxx来激活某一配置

##### Actuator

监控并管理应用程序
 监控：让我们去发现和了解程序的运行状况各种指标
 管理：比如说通过Actuator去做一个shutdown功能，通过访问一个特定的url去操作，默认是不开启的，另外 还可以在运行的过程中 对日志进行调整

需要在pom.xml中添加依赖

```xml
<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

application.yml

```yaml

server:
  port: 8080
  servlet:
    context-path: /demo
# 若要访问端点信息，需要配置用户名和密码
spring:
  security:
    user:
      name: xkcoding
      password: 123456
#管理 可以获取程序信息
management:
  # 端点信息接口使用的端口，为了和主系统接口使用的端口进行分离
  server:
    port: 8090
    servlet:
      context-path: /sys
  # 端点健康情况，默认值"never"，设置为"always"可以显示硬盘使用情况和线程情况
  endpoint:
    health:
      show-details: always
  # 设置端点暴露的哪些内容，默认["health","info"]，设置"*"代表暴露所有可访问的端点
  endpoints:
    web:
      exposure:
        include: '*'
```



参考：[Spring Boot Actuator官方文档](https://docs.spring.io/spring-boot/docs/2.3.3.RELEASE/reference/html/production-ready-features.html#production-ready-endpoints)	[常用endpoint的使用说明](https://blog.csdn.net/iechenyb/article/details/108075948)

##### Spring Boot Admin

它是用于监控springboot应用程序的监控系统，应用程序通过Apring Boot Admin Client进行注册（通过HTTP的方式），或者使用springcloud来发现（比如：eureka)，UI只是在Spring Boot Actuator端点上的一个AngularJs应用程序

需要在pom.xml中添加依赖

```xml
<!--客户端依赖-->
<dependency>
      <groupId>de.codecentric</groupId>
      <artifactId>spring-boot-admin-starter-client</artifactId>
</dependency>
<!--服务端依赖-->
<dependency>
      <groupId>de.codecentric</groupId>
      <artifactId>spring-boot-admin-starter-server</artifactId>
</dependency>

```


`@EnableAdminServer`

服务器端使用该注解用于导入Spring Boot Admin Server配置

客户端application.yml

```yaml
server:
  port: 8080
  servlet:
    context-path: /demo
spring:
  application:
    # Spring Boot Admin展示的客户端项目名，不设置，会使用自动生成的随机id
    name: spring-boot-demo-admin-client
  boot:
    admin:
      client:
        # Spring Boot Admin 服务端地址
        url: "http://localhost:8000/"
        instance:
          metadata:
            # 客户端端点信息的安全认证信息
            user.name: ${spring.security.user.name}
            user.password: ${spring.security.user.password}
  security:
    user:
      name: xkcoding
      password: 123456
management:
  endpoint:
    health:
      # 端点健康情况，默认值"never"，设置为"always"可以显示硬盘使用情况和线程情况
      show-details: always
  endpoints:
    web:
      exposure:
        # 设置端点暴露的哪些内容，默认["health","info"]，设置"*"代表暴露所有可访问的端点
        include: "*"
```

参考：[spring boot admin官方文档](https://codecentric.github.io/spring-boot-admin/2.1.0/)

##### logback

配置文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--根节点-->
<configuration>
  <!--用于定义变量-->
  <property name="FILE_ERROR_PATTERN"
            value="${FILE_LOG_PATTERN:-%d{${LOG_DATEFORMAT_PATTERN:-yyyy-MM-dd HH:mm:ss.SSS}} ${LOG_LEVEL_PATTERN:-%5p} ${PID:- } --- [%t] %-40.40logger{39} %file:%line: %m%n${LOG_EXCEPTION_CONVERSION_WORD:-%wEx}}"/>
  <include resource="org/springframework/boot/logging/logback/defaults.xml"/>
 <!--附加器，用于将日志事件传递到其目标-->
 <!--ConsoleAppender 在控制台显示-->
 <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
  <filter class="ch.qos.logback.classic.filter.LevelFilter">
   <level>INFO</level>
  </filter>
  <encoder>
   <pattern>${CONSOLE_LOG_PATTERN}</pattern>
   <charset>UTF-8</charset>
  </encoder>
 </appender>

 <!--RollingFileAppender滚动文件记录-->
 <appender name="FILE_INFO" class="ch.qos.logback.core.rolling.RollingFileAppender">
  <!--如果只是想要 Info 级别的日志，只是过滤 info 还是会输出 Error 日志，因为 Error 的级别高， 所以我们使用下面的策略，可以避免输出 Error 的日志-->
  <filter class="ch.qos.logback.classic.filter.LevelFilter">
   <!--过滤 Error-->
   <level>ERROR</level>
   <!--匹配到就禁止-->
   <onMatch>DENY</onMatch>
   <!--没有匹配到就允许-->
   <onMismatch>ACCEPT</onMismatch>
  </filter>
  <!--日志名称，如果没有File 属性，那么只会使用FileNamePattern的文件路径规则如果同时有<File>和<FileNamePattern>，那么当天日志是<File>，明天会自动把今天的日志改名为今天的日期。即，<File> 的日志都是当天的。-->
  <!--<File>logs/info.demo-logback.log</File>-->
  <!--滚动策略，按照时间滚动 TimeBasedRollingPolicy-->
  <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
   <!--文件路径,定义了日志的切分方式——把每一天的日志归档到一个文件中,以防止日志填满整个磁盘空间-->
   <FileNamePattern>logs/demo-logback/info.created_on_%d{yyyy-MM-dd}.part_%i.log</FileNamePattern>
   <!--只保留最近90天的日志-->
   <maxHistory>90</maxHistory>
   <!--用来指定日志文件的上限大小，那么到了这个值，就会删除旧的日志-->
   <!--<totalSizeCap>1GB</totalSizeCap>-->
   <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
    <!-- maxFileSize:这是活动文件的大小，默认值是10MB,本篇设置为1KB，只是为了演示 -->
    <maxFileSize>2MB</maxFileSize>
   </timeBasedFileNamingAndTriggeringPolicy>
  </rollingPolicy>
  <!--<triggeringPolicy class="ch.qos.logback.core.rolling.SizeBasedTriggeringPolicy">-->
  <!--<maxFileSize>1KB</maxFileSize>-->
  <!--</triggeringPolicy>-->
  <encoder>
   <pattern>${FILE_LOG_PATTERN}</pattern>
   <charset>UTF-8</charset> <!-- 此处设置字符集 -->
  </encoder>
 </appender>

 <appender name="FILE_ERROR" class="ch.qos.logback.core.rolling.RollingFileAppender">
  <!--如果只是想要 Error 级别的日志，那么需要过滤一下，默认是 info 级别的，ThresholdFilter-->
  <filter class="ch.qos.logback.classic.filter.ThresholdFilter">
   <level>Error</level>
  </filter>
  <!--日志名称，如果没有File 属性，那么只会使用FileNamePattern的文件路径规则如果同时有<File>和<FileNamePattern>，那么当天日志是<File>，明天会自动把今天的日志改名为今天的日期。即，<File> 的日志都是当天的。-->
  <!--<File>logs/error.demo-logback.log</File>-->
  <!--滚动策略，按照时间滚动 TimeBasedRollingPolicy-->
  <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
   <!--文件路径,定义了日志的切分方式——把每一天的日志归档到一个文件中,以防止日志填满整个磁盘空间-->
   <FileNamePattern>logs/demo-logback/error.created_on_%d{yyyy-MM-dd}.part_%i.log</FileNamePattern>
   <!--只保留最近90天的日志-->
   <maxHistory>90</maxHistory>
   <timeBasedFileNamingAndTriggeringPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedFNATP">
    <!-- maxFileSize:这是活动文件的大小，默认值是10MB,本篇设置为1KB，只是为了演示 -->
    <maxFileSize>2MB</maxFileSize>
   </timeBasedFileNamingAndTriggeringPolicy>
  </rollingPolicy>
  <encoder>
   <pattern>${FILE_ERROR_PATTERN}</pattern>
   <charset>UTF-8</charset> <!-- 此处设置字符集 -->
  </encoder>
 </appender>

 <root level="info">
  <appender-ref ref="CONSOLE"/>
  <appender-ref ref="FILE_INFO"/>
  <appender-ref ref="FILE_ERROR"/>
 </root>
</configuration>
```

参考：[Logback配置文件](https://www.cnblogs.com/gavincoder/p/10091757.html)  [Logback官方文档](https://logback.qos.ch/manual/)

#### AOP

AOP为Aspect Oriented Programming的缩写，意为：面向切面编程，通过预编译方式和运行期动态代理实现程序功能的统一维护的一种技术。

```xml
<dependency>
 <groupId>org.springframework.boot</groupId>
 <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

**概念定义**

- Aspect（切面）： Aspect 声明类似于 Java 中的类声明，在 Aspect 中会包含着一些 Pointcut 以及相应的 Advice。
- Joint point（连接点）：表示在程序中明确定义的点，典型的包括方法调用，对类成员的访问以及异常处理程序块的执行等等，它自身还可以嵌套其它 joint point。
- Pointcut（切点）：表示一组 joint point，这些 joint point 或是通过逻辑关系组合起来，或是通过通配、正则表达式等方式集中起来，它定义了相应的 Advice 将要发生的地方。
- Advice（增强）：Advice 定义了在 Pointcut 里面定义的程序点具体要做的操作，它通过 before、after 和 around 来区别是在每个 joint point 之前、之后还是代替执行的代码。
- Target（目标对象）：织入 Advice 的目标对象.。
- Weaving（织入）：将 Aspect 和其他对象连接起来, 并创建 Adviced object 的过程

在AOP中切面就是与业务逻辑独立，但又垂直存在于业务逻辑的代码结构中的通用功能组合；切面与业务逻辑相交的点就是切点；连接点就是把业务逻辑离散化后的关键节点；切点属于连接点，是连接点的子集；Advice（增强）就是切面在切点上要执行的功能增加的具体操作；在切点上可以把要完成增强操作的目标对象（Target）连接到切面里，这个连接的方式就叫织入。

简单总结（不一定恰当）：对所有符合规则的一些方法做拦截，先执行我自定义的方法，再执行被拦截的方法（这个先后有多种形式）

##### Pointcut

格式：@Pointcut(execution(modifiers-pattern? ret-type-pattern declaring-type-pattern? name-pattern(param-pattern)throws-pattern?) )

- 修饰符匹配（modifier-pattern?）
- 返回值匹配（ret-type-pattern）可以为*表示任何返回值,全路径的类名等
- 类路径匹配（declaring-type-pattern?）
- 方法名匹配（name-pattern）可以指定方法名 或者 *代表所有, set* 代表以set开头的所有方法
- 参数匹配（(param-pattern)）可以指定具体的参数类型，多个参数间用“,”隔开，各个参数也可以用“*”来表示匹配任意类型的参数，如(String)表示匹配一个String参数的方法；(*,String) 表示匹配有两个参数的方法，第一个参数可以是任意类型，而第二个参数是String类型；可以用(..)表示零个或多个任意参数
- 异常类型匹配（throws-pattern?）
- 其中后面跟着“?”的是可选项

例：

```java
//Pointcut表示式
@Pointcut("execution(public * com. savage.service.UserService.*(..))")
//Point签名 主要是方便之后的使用 相当于取个名字
private void log(){}
```

public 修饰符	*返回值	com. savage.service.UserService 类路径	*方法名	(..)返回值

##### Advice

- before advice, 在 join point 前被执行的 advice. 虽然 before advice 是在 join point 前被执行, 但是它并不能够阻止 join point 的执行, 除非发生了异常(即我们在 before advice 代码中, 不能人为地决定是否继续执行 join point 中的代码)
- after return advice, 在一个 join point 正常返回后执行的 advice
-  after throwing advice, 当一个 join point 抛出异常后执行的 advice
-  after(final) advice, 无论一个 join point 是正常退出还是发生了异常, 都会被执行的 advice.
-  around advice, 在 join point 前和 joint point 退出后都执行的 advice. 这个是最常用的 advice.
-  introduction，introduction可以为原有的对象增加新的属性和方法。

正确理解around

```java
    @Around(value = "test.PointCuts.aopDemo()")
    public Object around(ProceedingJoinPoint pjp) throws  Throwable{
        System.out.println("[Aspect1] around advise 1");	//joint point之前运行
        Object result = pjp.proceed();
        System.out.println("[Aspect1] around advise2");		//joint point之后运行
        return result;
    }
```

参考：[Spring 官方文档AOP](https://docs.spring.io/spring-framework/docs/current/reference/html/core.html#aop)



#### 统一异常处理

使用一个类统一的处理异常

1. 添加注解`@ControllerAdvice`
2. 使用`@ExceptionHandler(value = JsonException.class)`处理异常
3. 两种方式 返回json数据    跳转到异常界面

##### ModelAndView（用来实现异常界面的跳转）

简单理解它是将后台返回的数据传递给View层，同时包含一个要访问的View层的URL地址

作用

- 设置转向地址
- 将底层获取的数据进行存储（或者封装）
- 最后将数据传递给View

```java
ModelAndView view = new ModelAndView();
view.addObject("message", exception.getMessage());
view.setViewName(DEFAULT_ERROR_VIEW);
return view;
```



#### Spring Boot 集成模板引擎

Controller + modelAndView 

`@PostMapping()`方法自动将post数据转化为函数参数

```java
@PostMapping("/login")
public ModelAndView login(User user, People people, HttpServletRequest request) {
	...
}
```

通过modelAndView中addObject方法向html文件插入动态数据

这部分有点迷茫 待补充+++



#### Spring Boot 集成数据库

##### Jdbc Template

依赖

```java
<dependency>
 <groupId>org.springframework.boot</groupId>
 <artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>
<dependency>
 <groupId>mysql</groupId>
 <artifactId>mysql-connector-java</artifactId>
</dependency>
```
泛型转化为真实类型

```java
//Class Object<T>
//用于获得T的class对象
//这句话的原理不清楚
clazz = (Class<T>) ((ParameterizedType) getClass().getGenericSuperclass()).getActualTypeArguments()[0];
```

`@PathVariable("xxx")`
通过 @PathVariable 可以将URL中占位符参数{xxx}绑定到处理器类的方法形参中@PathVariable(“xxx“) 

##### 自定义注解

`@Retention({RetentionPolicy.Runtime}) `

用来指定保留注解的策略，RetentionPolicy这个枚举类型的常量描述保留注释的各种策略

RetentionPolicy.SOURCE   //注解仅存在于源码中，在class字节码文件中不包含

RetentionPolicy.CLASS     // 默认的保留策略，注解会在class字节码文件中存在，但运行时无法获得，

RetentionPolicy.RUNTIME  // 注解会在class字节码文件中存在，在运行时可以通过反射获取到


`@Target({ElementType.TYPE})`

用来指定在何处写入注解的合法位置

ElementType.TYPE  	 接口、类、枚举

ElementType.FIELD	 字段、枚举的常量

ElementType.METHOD 	方法

ElementType.PARAMETER	方法参数

ElementType.CONSTRUCTOR	构造函数

ElementType.LOCAL_VARIABLE	局部变量

ElementType.ANNOTATION_TYPE	注解

ElementType.PACKAGE 	包

##### 测试类

需要给测试类添加`@Component`注解

并在需要注入的对象上添加@Autowired实现自动注入

？？？为什么这样做的缘由尚不明白？？？

##### Mybatis

`@Mapper`

1. 用来生成mapper映射文件
2. 给接口自动生成实现类
3. 将该类交由Spring进行管理

`@Param`

用于Mybatis传递参数

`@MapperScan`

指定要变成实现类的接口所在的包，然后包下面的所有接口在编译之后都会生成相应的实现类，相当于多个`@Mapper`

`@EnableTransactionManagement`

用于Spring Boot开启事务支持

Mybatis-plus

- DAO层 自动生成Mapper映射`extends BaseMapper<T>`

- Service层 自动实现CURD操作`extends IService<T>` `extends ServiceImpl<TMapper, T>`
- 对项目进行config配置

`@Primary`

在有多个选择时，作为首选

数据库连接池
数据库连接池负责分配、管理和释放数据库连接，它允许应用程序重复使用一个现有的数据库连接，而不是再重新建立一个；释放空闲时间超过最大空闲时间的数据库连接来避免因为没有释放数据库连接而引起的数据库连接遗漏。这项技术能明显提高对数据库操作的性能。





