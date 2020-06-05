#include <WiFi.h>

const char* ssid = "XXXXXXXXX";
const char* password = "XXXXXXXXX"; 
 
// Server
const char* ip   = "192.168.1.XXX";
const int port = 8080;
const char* path   = "/";

WiFiClient client;



void http_post(){
  char buf[]="";
  //送信するデータをbufに書き込む。
  sprintf(buf,"hoge\n");
  
  if (!client.connect(ip, port)) {
    Serial.println("post_disconnect");
    return;
  }

  
  client.printf("POST %s HTTP/1.1\n",path);
  client.print(F("Host: "));client.println(ip);
  client.println(F("Connection: close"));
  client.print(F("Content-Length: "));client.println(strlen(buf));        
  client.println();
  client.print(buf);


  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 10000) {
      Serial.println("post_timeout");
      client.stop();
      return;
    }
  }
  String ret_data;

  while (client.available()) {
    char retn_c = client.read();
    ret_data += retn_c;
  }
  if (ret_data.indexOf("OK") != -1){
    Serial.println("post_connect_OK");

  }else if (ret_data.indexOf("NG") != -1){
    Serial.println("post_connect_NG");
  }
}


void setup() {
  Serial.begin(9600);
  delay(10);
 
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
 
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
     
}

void loop() {
  http_post();
  delay(10000);
}
