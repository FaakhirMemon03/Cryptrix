import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(CryptrixApp());
}

class CryptrixApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CRYPTRIX | OS',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: Color(0xFF000800),
        primaryColor: Color(0xFF00FF41), // Matrix Green
        hintColor: Color(0xFF00FF41),
        fontFamily: 'Courier', // Hacker font
      ),
      home: LoginScreen(),
    );
  }
}

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _idController = TextEditingController();
  bool _isAccessing = false;

  void _bypassSecurity() {
    if (_idController.text.isEmpty) return;
    setState(() => _isAccessing = true);
    Future.delayed(Duration(seconds: 2), () {
      setState(() => _isAccessing = false);
      Navigator.push(context, MaterialPageRoute(builder: (context) => TerminalDashboard(deviceId: _idController.text)));
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text("--- SYSTEM ACCESS REQ ---", style: TextStyle(color: Color(0xFF00FF41), letterSpacing: 2)),
              SizedBox(height: 30),
              Container(
                width: 150,
                height: 150,
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: Color(0xFF00FF41), width: 2),
                  boxShadow: [BoxShadow(color: Color(0xFF00FF41).withOpacity(0.3), blurRadius: 20)],
                ),
                child: Icon(Icons.qr_code_scanner, size: 80, color: Color(0xFF00FF41)),
              ),
              SizedBox(height: 40),
              Text("IDENTIFY TARGET DEVICE", style: TextStyle(color: Color(0xFF00FF41), fontSize: 18, fontWeight: FontWeight.bold)),
              SizedBox(height: 20),
              Container(
                width: 300,
                child: TextField(
                  controller: _idController,
                  style: TextStyle(color: Color(0xFF00FF41)),
                  decoration: InputDecoration(
                    prefixIcon: Icon(Icons.terminal, color: Color(0xFF00FF41)),
                    hintText: "Enter IP Address...",
                    hintStyle: TextStyle(color: Color(0xFF00FF41).withOpacity(0.5)),
                    enabledBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF00FF41))),
                    focusedBorder: OutlineInputBorder(borderSide: BorderSide(color: Color(0xFF00FF41), width: 2)),
                  ),
                ),
              ),
              SizedBox(height: 30),
              _isAccessing 
                ? Column(children: [CircularProgressIndicator(color: Color(0xFF00FF41)), SizedBox(height: 10), Text("BYPASSING FIREWALL...", style: TextStyle(color: Color(0xFF00FF41), fontSize: 10))])
                : OutlinedButton(
                    onPressed: _bypassSecurity,
                    style: OutlinedButton.styleFrom(
                      side: BorderSide(color: Color(0xFF00FF41)),
                      padding: EdgeInsets.symmetric(horizontal: 50, vertical: 20),
                    ),
                    child: Text("ESTABLISH CONNECTION", style: TextStyle(color: Color(0xFF00FF41))),
                  ),
            ],
          ),
        ),
      ),
    );
  }
}

class TerminalDashboard extends StatefulWidget {
  final String deviceId;
  TerminalDashboard({required this.deviceId});

  @override
  _TerminalDashboardState createState() => _TerminalDashboardState();
}

class _TerminalDashboardState extends State<TerminalDashboard> {
  List<String> logs = ["tunnel_active: TRUE", "sys_status: ENCRYPTED"];

  Future<void> _sendCommand(String action, [Map<String, dynamic>? params]) async {
    setState(() {
      logs.add("> EXECUTING: $action...");
    });

    try {
      // Assuming deviceId is the IP address
      final url = Uri.parse('http://${widget.deviceId}:5050');
      final response = await http.post(
        url,
        body: jsonEncode({
          "action": action,
          "params": params ?? {},
          "deviceId": widget.deviceId,
        }),
        headers: {"Content-Type": "application/json"},
      ).timeout(Duration(seconds: 5));

      if (response.statusCode == 200) {
        setState(() {
          logs.add("> SUCCESS: Command $action received.");
        });
      } else {
        setState(() {
          logs.add("> ERROR: Server returned ${response.statusCode}");
        });
      }
    } catch (e) {
      setState(() {
        logs.add("> CRITICAL_ERROR: $e");
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("> CRYPTRIX_OS: ${widget.deviceId}", style: TextStyle(color: Color(0xFF00FF41), fontSize: 14)),
        backgroundColor: Colors.black,
        elevation: 0,
        actions: [IconButton(icon: Icon(Icons.power_settings_new, color: Colors.red), onPressed: () => Navigator.pop(context))],
      ),
      body: Container(
        padding: EdgeInsets.all(10),
        child: Column(
          children: [
            _buildTerminalLog(),
            SizedBox(height: 10),
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 10,
                mainAxisSpacing: 10,
                childAspectRatio: 1.5,
                children: [
                  _buildHackerBtn("LOCK", Icons.lock_outline, Colors.blue),
                  _buildHackerBtn("SNAPSHOT", Icons.camera_rear, Colors.cyan),
                  _buildHackerBtn("KILL_NET", Icons.wifi_off, Colors.orange), // Note: disable_wifi in agent
                  _buildHackerBtn("RESTART", Icons.restart_alt, Colors.purple),
                  _buildHackerBtn("FACTORY_RESET", Icons.delete_forever, Colors.red),
                  _buildHackerBtn("GET_INFO", Icons.location_on, Colors.green),
                ],
              ),
            ),
            _buildPanicMode(),
          ],
        ),
      ),
    );
  }

  Widget _buildTerminalLog() {
    return Container(
      width: double.infinity,
      height: 120,
      padding: EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: Colors.black,
        border: Border.all(color: Color(0xFF00FF41).withOpacity(0.5)),
      ),
      child: ListView.builder(
        itemCount: logs.length,
        itemBuilder: (context, index) {
          return Text(logs[index], style: TextStyle(color: Color(0xFF00FF41), fontSize: 10));
        },
      ),
    );
  }

  Widget _buildHackerBtn(String action, IconData icon, Color color) {
    return InkWell(
      onTap: () => _sendCommand(action),
      child: Container(
        decoration: BoxDecoration(
          border: Border.all(color: Color(0xFF00FF41).withOpacity(0.3)),
          color: Colors.black,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: Color(0xFF00FF41), size: 30),
            SizedBox(height: 5),
            Text(action, style: TextStyle(color: Color(0xFF00FF41), fontSize: 10, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  Widget _buildPanicMode() {
    return Container(
      width: double.infinity,
      height: 70,
      margin: EdgeInsets.symmetric(vertical: 10),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.red.withOpacity(0.2),
          side: BorderSide(color: Colors.red, width: 2),
        ),
        onPressed: () => _sendCommand("PANIC_MODE"),
        child: Text("!!! EMERGENCY_LOCKDOWN !!!", style: TextStyle(color: Colors.red, fontWeight: FontWeight.bold, letterSpacing: 2)),
      ),
    );
  }
}

