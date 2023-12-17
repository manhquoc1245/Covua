- Cài đặt SQL server, chạy sql ChessDB để tạo cơ sở dữ liệu

###Nếu kết nối thông qua mạng LAN
* Phía server 
- Vào file settingServer.txt sửa đổi
- localHost để là no, port có thể để nguyên hoặc chọn 1 cổng khác bất kì từ 0 đến 65534 sao cho cổng đấy chưa bị sử dụng bởi các chương trình khác, serverDatabaseName là tên của SQL Server database chứa CSDL người dùng.
- Bật server.exe phía server

* Phía người chơi
- Vào file setting.txt sửa
- server để là địa chỉ IP của máy tính bật server, phần port để số đúng số port đã đặt bên server
- Bật game.exe

###Nếu kết nối thông qua ngrok
- Tải ngrok về máy sử dụng làm máy chủ. Lưu ý: bạn có thể đăng ký ngrok trên website của hãng để có kết nối không giới hạn thời gian
* Phía server 
- Theo đó localHost để là yes, port và serverDatabaseName để tương tự như khi kết nối mạng LAN.
- Copy file ngrok.exe đưa vào cùng folder với file server.exe, chạy ngrok.exe
- Nhập ngrok.exe tcp <số port dùng để kết nối>
- Chú ý giá trị ở dòng Forwarding có dạng 0.tcp.in.ngrok.io:12080
- Bật server.exe phía server

* Phía người chơi
- Vào file setting.txt sửa
- server và port thay thế bằng 2 giá trị có được từ ngrok
VD: 
server:0.tcp.in.ngrok.io
port:12080
- Bật game.exe