import 'package:flutter/material.dart';

void main() {
  runApp(CryptrixApp());
}

class CryptrixApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Cryptrix Remote',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Colors.redAccent,
        hintColor: Colors.amber,
        fontFamily: 'Roboto',
      ),
      home: DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('CRYPTRIX | SECURITY'),
        centerTitle: true,
        backgroundColor: Colors.black,
      ),
      body: Container(
        padding: EdgeInsets.all(16.0),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.black87, Colors.red[900]!],
          ),
        ),
        child: Column(
          children: [
            _buildStatusHeader(),
            SizedBox(height: 20),
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                crossAxisSpacing: 10,
                mainAxisSpacing: 10,
                children: [
                  _buildCommandCard(context, 'LOCK SCREEN', Icons.lock, Colors.blue),
                  _buildCommandCard(context, 'SNAPSHOT', Icons.camera_alt, Colors.green),
                  _buildCommandCard(context, 'INFO', Icons.info, Colors.cyan),
                  _buildCommandCard(context, 'BLOCK INPUT', Icons.block, Colors.orange),
                  _buildCommandCard(context, 'SHUTDOWN', Icons.power_settings_new, Colors.red),
                  _buildCommandCard(context, 'RESTART', Icons.restart_alt, Colors.purple),
                ],
              ),
            ),
            _buildPanicButton(context),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusHeader() {
    return Card(
      color: Colors.white10,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            CircleAvatar(backgroundColor: Colors.green, radius: 8),
            SizedBox(width: 10),
            Text('Agent Online: PC-AGENT-001', style: TextStyle(color: Colors.white70)),
            Spacer(),
            Icon(Icons.refresh, color: Colors.white54),
          ],
        ),
      ),
    );
  }

  Widget _buildCommandCard(BuildContext context, String label, IconData icon, Color color) {
    return InkWell(
      onTap: () => _sendCommand(label),
      child: Card(
        color: Colors.white.withOpacity(0.05),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 40, color: color),
            SizedBox(height: 10),
            Text(label, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
          ],
        ),
      ),
    );
  }

  Widget _buildPanicButton(BuildContext context) {
    return Container(
      width: double.infinity,
      height: 60,
      margin: EdgeInsets.only(top: 20),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.redAccent,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
          elevation: 10,
        ),
        onPressed: () => _confirmPanic(context),
        child: Text(
          'EMERGENCY PANIC MODE',
          style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
        ),
      ),
    );
  }

  void _sendCommand(String command) {
    print("Command Sent: $command");
    // In a real app, this would call a Firebase/Supabase API
  }

  void _confirmPanic(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Initiate Lockdown?'),
        content: Text('This will disable internet, lock inputs, and encrypt sensitive data on the target PC.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: Text('CANCEL')),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () {
              _sendCommand('PANIC_MODE');
              Navigator.pop(context);
            },
            child: Text('EXECUTE'),
          ),
        ],
      ),
    );
  }
}
