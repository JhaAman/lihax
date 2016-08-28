using System;
using UnityEngine;
using System.Collections;
using System.Net.Sockets;
using System.Net;

public class NewBehaviourScript : MonoBehaviour {

	public Socket sock;
	public IPAddress hostIP;
	public IPEndPoint ep;

	public byte[] speedAndSteering;
	public float speed;
	public float steering;

	// Use this for initialization
	void Start () {
		sock = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);

		// A better way of obtaining your IP address **ONLY IF YOU ARE CONNECTED TO A NETWORK**: 

		IPAddress[] ipv4Addresses = Array.FindAll(
			Dns.GetHostEntry(Dns.GetHostName()).AddressList,
			a => a.AddressFamily == AddressFamily.InterNetwork);
		hostIP = ipv4Addresses [0];

		// This will setup your socket if you **ARE NOT** connected to any network: 

		// hostIP = IPAddress.Parse("127.0.0.1");

		ep = new IPEndPoint(hostIP, 6510);
		print ("Opening a udp socket at: " + ep);
		sock.Bind(ep); 
		sock.Receive(speedAndSteering);
	}
	
	// Update is called once per frame
	void Update () {
		speed = System.BitConverter.ToSingle (speedAndSteering, 0);
		steering = System.BitConverter.ToSingle (speedAndSteering, 4);
	}
}
