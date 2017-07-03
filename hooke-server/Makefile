main:svr/server.cc core.so protocol.so channel.so client
	g++ -stdlib=libstdc++ -g -o main svr/server.cc protocol/services.pb.h kernel/hooke-server.h -lpthread -lprotobuf -L/usr/local/lib-Llibs -lcore -lprotocol -lchannel -I/usr/local/include
client:clt/client.cc core.so protocol.so channel.so
	g++ -stdlib=libstdc++ -g -o client clt/client.cc protocol/services.pb.h kernel/hooke-client.h -lpthread -L/usr/local/lib -Llibs -lcore -lprotocol -lchannel -I/usr/local/include -static -levent
core.so:kernel/hooke-server.cc kernel/hooke-server.h kernel/channel.h kernel/channel.cc kernel/hooke-client.cc kernel/hooke-client.h
	g++ -stdlib=libstdc++ -g -shared -fPIC -o libs/libcore.so kernel/hooke-server.cc kernel/hooke-client.cc -I/usr/local/include -L/usr/local/lib -static -levent
channel.so:kernel/channel.cc kernel/channel.h
	g++ -stdlib=libstdc++ -g -c -shared -fPIC -o libs/libchannel.so kernel/channel.cc -I /usr/local/include -L/usr/local/lib -static -levent
protocol.so:protocol/services.pb.cc protocol/services.pb.h
	g++ -stdlib=libstdc++ -g -c -shared -fPIC -o libs/libprotocol.so protocol/services.pb.cc -I /usr/local/include -L/usr/local/lib
