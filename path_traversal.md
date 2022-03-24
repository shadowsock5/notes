### 漏洞代码
```java
    private String uploadExcelFile(MultipartFile file)throws Exception{
        String fileName = System.currentTimeMillis() +"_"+file.getOriginalFilename();    // 获取当前系统时间戳与文件名拼接
        String basePath = "D:\\repos\\xxx\upload\\";
        File newFile = new File(basePath+fileName);

        // 父目录不存在，会创建
        if (!newFile.getParentFile().exists()){
            newFile.getParentFile().mkdirs();
        }
        
        // 文件不存在，会创建
        if (!newFile.exists()){
            newFile.createNewFile();
        }
        Files.write(file.getBytes(), newFile);    // 写入文件
        
        return basePath+fileName;
    }
```


### 修复代码
// 这里是参照[CVE-2019-3398](https://xz.aliyun.com/t/4854)的修复方式来的。
File#getName方法仅取文件名的最后部分。参考：https://docs.oracle.com/javase/8/docs/api/java/io/File.html#getName--

```java
    private String uploadExcelFile(MultipartFile file)throws Exception{
        String fileName = System.currentTimeMillis() +"_"+file.getOriginalFilename();
        String basePath = "D:\\repos\\xxx\\upload\\";
        
        // 这里是参照CVE-2019-3398的修复方式来的。File#getName方法仅取文件名的最后部分。参考：https://docs.oracle.com/javase/8/docs/api/java/io/File.html#getName--
        File newFile = new File(basePath+(new File(fileName)).getName());
        

        if (!newFile.getParentFile().exists()){
            newFile.getParentFile().mkdirs();
        }
        if (!newFile.exists()){
            newFile.createNewFile();
        }
        Files.write(file.getBytes(), newFile);
        
        return newFile.getName();
    }
```
