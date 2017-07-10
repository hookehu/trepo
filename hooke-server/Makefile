main:svr/server.cc core.so protocol.so channel.so client
	g++ -g -o main svr/server.cc protocol/services.pb.h -lpthread -L/usr/local/lib -lprotobuf -Llibs -lcore -lprotocol -lchannel -I/usr/local/include -Wl,-rpath=/usr/local/lib,-rpath=./libs
client:clt/client.cc core.so protocol.so channel.so
	g++ -g -o client clt/client.cc protocol/services.pb.h -lpthread -L/usr/local/lib -lprotobuf -Llibs -lcore -lprotocol -lchannel -I/usr/local/include -Wl,-rpath=/usr/local/lib,-rpath=./libs
core.so:kernel/net.cc kernel/net.h kernel/channel.h kernel/channel.cc
	g++ -g -shared -fPIC -o libs/libcore.so kernel/net.cc -I/usr/local/include -L/usr/local/lib
channel.so:kernel/channel.cc kernel/channel.h
	g++ -g -c -shared -fPIC -o libs/libchannel.so kernel/channel.cc -I /usr/local/include -L/usr/local/lib
protocol.so:protocol/services.pb.cc protocol/services.pb.h
	g++ -g -c -shared -fPIC -o libs/libprotocol.so protocol/services.pb.cc -I /usr/local/include -L/usr/local/lib
