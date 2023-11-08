
## 注意！！！！本项目没有适配 mac m1 m2 芯片

## 配置文件
配置文件位于项目根目录的 `config.txt.yaml` 中。请根据实际情况修改最后四行。
具体的修改说明已在 `config.txt.yaml` 文件中进行了注释。
> 注意：由于海内外网络环境的差异，请特别关注 `openai` 的 proxy 和 host 是否可访问。
> 此外在 dockerfile 中各种 add pip 等已经换源，如在海外请酌情修改。

## 启动方式
1. 打开文件根目录下的 `config.txt.yaml` 文件，查看是否需要修改最后四行（不改也可以）。
2. 启动docker，命令如下：
```
docker-compose up --build

之后访问 http://localhost:8000/goods_search/ui/ 可以看到swagger-ui文档，
```
> 注意：由于安装了pandas等计算库可能耗费较长时间，构建过程可能需要一些时间。
> 第一次build耗时很长，可以先 docker pull homebrew/ubuntu20.04 提前 pull 镜像。

3. 访问 http://localhost:8000/goods_search/ui/ 可以看到swagger-ui文档。
4. 对于query查询接口，直接输入关键词后页面点击 try 按钮即可测试

## 项目对外依赖
- MySQL: 该项目使用外部 MySQL 数据库服务。这里是我配置的一个数据库，根据实际情况可能需要进行修改。
- openai: 在向量数据库相关逻辑中使用了 openai （用来 embedding）。由于海内外上网环境的差异，我在配置文件中修改了 `openai_api_key` 和 `openai_api_base`。
- 当前使用的代理是付费的，对于我的测试数据来说足够使用。如果无法使用，请更换 `openai` 的代理和密钥。

## 中心思想
- 对于搜索功能，使用redisearch的索引进行查询。
- 如果查询不到结果，则设置模糊查询后重新搜索。
- 如果仍然无法找到结果，则会使用向量数据库（可以保证始终能找到最相似的结果，但效果需要评估）。
- 此外，还编写了推荐商品的接口。该接口是另外独立的，需要调用方根据需要灵活判断是否使用。

## TODO
1. 接口还未实现分页功能。
2. 以上技术栈均支持额外的负载过滤器。
3. 对于 openai 的 embedding 功能，目前是收费 + 使用redis缓存的方式。可以考虑使用免费的 embedding 服务。
4. 推荐数据需要定期更新。
5. 由于时间紧迫，Docker 部署比较简单，安装了一些不必要的软件。
