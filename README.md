# pykv
easy key/value save package

可根据需要灵活使用各种k-v存储

# 用法

import pykv
pykv.KvFactory.new(db_uri)

db_uri可选值:
	redis://localhost:6379
	mysql://localhost:3306
	mongodb://localhost:27017
	leveldb://localhost/opt/cache.db
	file://localhost/opt/cache.db
	mem://localhost

