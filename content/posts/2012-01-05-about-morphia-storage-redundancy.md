title: 关于Morphia在存储冗余类的时候出现的一个问题？
category: Java
tags: java, morphia, code, mongo
Date: 2012-01-05

昨天中午临吃午饭前，我对系统的业务功能代码进行重构之后，准备测试一下，通过就去吃饭，但是发生了一个让我很意外的问题，就是在存储的时候，系统 报出来，类型转换异常（`java.lang.ClassCaseException`）或者是这么一个错误信息（`object is not an instance of declaring class`），很纠结因为之前这里测试都好好的，而且给内容组，视频组和测试组部署的测试环境，还在正常运行，一时想不通那里出了问题。

在 经过几次debug跟踪之后发现，每次报错都是在，存储FreeCourse和FreeVideo两个类是发生的问题，我仔细回忆 了，从上次重部署测试环境到出问题之间修改的代码，中间都没有什么问题，只有一个地方和其他人写的代码略有不一样，就是：其他人在写list类型的属性 时，默认是给空值的，但是我会给他们new一个size为0的ArrayList，这是我的一个喜欢，是为了避免出现一些因为疏忽而发生的问题，但是如果 只是这样不应该会有问题。

我 又仔细的看了一边相关业务代码和实体类的代码，所有代码中都没有问题，但是有一点和其他人的不同，就是我的FreeVideo下有个字段 videoInfos他的类型是`List<VideoInfo>`，而VideoInfo只有一个地方和其他的实体类不一样，就是没有去继承实 体类的基类MongoBaseEntity，但是这样也不应该有问题，但是问题应该和存储VideoInfo有关。

刚刚忘记说了我们系统 的 基本情况，现在这里简单的补充一下，我们使用的是mongodb，使用morphia做mongodb的数据操作，为了方便数据的查询，我在 FreeCourse冗余了FreeVideo，在FreeVideo冗余VideoInfo，FreeCourse包含多个 FreeVideo，FreeVideo包含多个VideoInfo，是个3层的1对多关系。

所以我继续深入的跟踪在存储 FreeCourse和FreeVideo时存储VideoInfo时的情况，在跟踪到存储冗余的VideoInfo时发现，在存储的时候回去调用一些方 法，这些方法的功能是处理BigDecimal，但是在VideoInfo中没有这些方法，而是在MongoBaseEntity中有这些方法，且这些方 法都加了`@PrePersist`，`@PostPersist`，`@PreLoad`等注解，也就是说只有继承了MongoBaseEntity的实体在存储前 后会调用这些方法，但是VideoInfo并没有继承MongoBaseEntity拿也就不应该调用这些方法啊，什么会去调用这些方法的？这个问题让我 很疑惑！

在几次跟踪之后融然无果的情况下，去找了我的头（也就是我们的技术经理），他也用同样的方法得到了同样的结论，但是他之后又跟踪 了 在服务器启动的时候Morphia对实体类的加载情况（不得不佩服下俺头，俺为啥就么想到呢）在跟踪Morphia在启动时对实体类的加载的时候发 现，Morphia会对每个实体类添加被注解的那些方法，而对非MongoBaseEntity子类则不处理，但是有个很奇怪地方我没有理解`com.google.code.morphia.mapping.MappedClass`的134行：

```java
for (Class<?> cls : lifecycleClasses) {
  for (Method m : ReflectionUtils.getDeclaredAndInheritedMethods(cls)) {
    for(Class<? extends Annotation> c : lifecycleAnnotations) {
      if (m.isAnnotationPresent(c)) {
        addLifecycleEventMethod(c, m, cls.equals(clazz) ? null : cls);
      }
    }
  }
}
```

在调用addLifecycleEventMethod的时候最后一个参数一定是空，虽然不知道是不是这个地方的问题，但是觉得很奇怪，我们先不管这里，先继续下去，在后面的跟踪当中并没有看到morphia为VideoInfo添加MongoBaseEntity中的注解方法，到这里发现貌似错误和morphia的实体类加载没有关系，拿是那里的问题呢？不得以我们有回到原点，再次跟踪了在存储FreeCourse代码，这次有一个被之前忽略的问题！

在跟踪到com.google.code.morphia.mapping.MappedClass的904行：

```java
mc.callLifecycleMethods(PostPersist.class, ent, dbO, mapr);
```

即上面哪行代码的时候，有两个参数让我注意到，第一个是entity他是FreeCourse，第二个是ent他缺失VideoInfo，在进入callLiftcycleMoethods方法内,跟踪到306行有下面两张截图：

![FzwYz](/file/images/FzwYz.png)
![KSLXG](/file/images/KSLXG.png)

下面两个图第一个是method.invoke方法的entity参数的值是VideoInfo，第二章图是method那个方法在调用，可以看到是MongoBaseEntity下的注解方法，也就是处理数据存储前后的事件方法。这里的VideoInfo是FreeCourse下冗余的FreeVideo下冗余的VideoInfo的数据。

从这里可以看到，morphia在存储冗余数据的时候，回去调用其上层类的注解方法，但是却是在使用method的invoke方法进行调用，并没有处理如果被冗余的实体如果没有次注解方法的问题，所以抛出了一个类型异常，在之后的测试发现这个异常并不影响morphia的存储，数据依然可以正确的保存到数据库中，不明白morphia为什么要这么做，既然没有影响存储，为什么还要抛出一个异常，难道只是为了提醒使用者，这样的结构是一个危险的方法，需要使用者自己进行处理？不管是什么原因，我最后的解决办法是为VideoInfo继承了MongoBaseEnity这样就不会在报出那个异常了。
