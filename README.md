# pykv
easy key/value save package

可根据需要灵活使用各种k-v存储

# 用法

	import pykv
	kv = pykv.KvFactory.new(uri)

	err = kv.set('k', 'v')
	v, err = kv.get('k')

	err = kv.mset({'a': 'b', 'c': 'd'})
	kvs, err = kv.mget(['a', 'b', 'c'])

	err是各步操作的结果，为None表示操作成功

	uri可选值参考:
	使用redis存储: redis://localhost:6379
	使用mysql存储: mysql://localhost:3306
	使用mongodb存储: mongodb://localhost:27017
	使用leveldb存储: leveldb://localhost/opt/cache.db
	使用文件存储: file://localhost/opt/cache.db
	内存缓存: mem://localhost

