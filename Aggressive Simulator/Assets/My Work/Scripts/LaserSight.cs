using UnityEngine;
using UnityEditor;
using System.Collections;
using System.IO;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

[RequireComponent (typeof (LineRenderer))]
public class LaserSight : MonoBehaviour {

	public float currentDistance = 0;
	public float currentRotation;

	public Transform pointOfOrigin;

	public bool LaserVisible = false;
	private LineRenderer lr;

	public float totalAngleDesired = 270f;
	public float angleIncrement = .25f;

	public Vector2[] distances;
	int totalAngleIncremented; 

	int frameNumber = 0;

	public Socket dataSenderOne;
	public IPAddress hostIP;
	public IPEndPoint epOne;
	public Socket dataSenderTwo;
	public IPEndPoint epTwo;


	void Start () {
		lr = GetComponent<LineRenderer>();

		totalAngleIncremented = (int) (totalAngleDesired/ angleIncrement); //i.e: 270 into half angles - 270/.5 = 540
		distances = new Vector2[totalAngleIncremented];

		dataSenderOne = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
		dataSenderTwo = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);

		IPAddress[] ipv4Addresses = Array.FindAll(
			Dns.GetHostEntry(Dns.GetHostName()).AddressList,
			a => a.AddressFamily == AddressFamily.InterNetwork);
		hostIP = ipv4Addresses [0];

		epOne = new IPEndPoint(hostIP, 5510);
		print ("Opening a udp socket at: " + epOne);
		dataSenderOne.Connect(epOne); 

		epTwo = new IPEndPoint(hostIP, 5520);
		print ("Opening a udp socket at: " + epTwo);
		dataSenderTwo.Connect(epTwo); 
	}

	void Update () {
		var fileName = "Frame.txt";
		RaycastHit Hit;

		/*if (Physics.Raycast(pointOfOrigin.position, pointOfOrigin.forward, out Hit)) {
			currentDistance = Hit.distance;
			if(Hit.collider){
				//lr.SetPosition(1, new Vector3 (0, 0, currentDistance));
			}
		} else {
			currentDistance = 0;
			//lr.SetPosition(1, new Vector3 (0, 0, 5000));
		}*/

		//Angle 0 is set at the center, so this takes the desired angle and goes -half of it
		//then changes the point of origin's rotation to match that initial angle
		Vector3 initialFrameAngleVector = pointOfOrigin.localEulerAngles;
		float currentAngle = -0.5f * totalAngleDesired;
		initialFrameAngleVector.y = currentAngle;
		pointOfOrigin.localEulerAngles = initialFrameAngleVector;

		using (StreamWriter sw = new StreamWriter (fileName)) {
			byte[] msg = new byte[4320];
			for (int i = 0; i < totalAngleIncremented; i++) {
				//send a raycast at current angle
				if (Physics.Raycast (pointOfOrigin.position, pointOfOrigin.forward, out Hit)) {
					currentDistance = Hit.distance;
					//assign distance to the Vector2 list:
					distances [i] = new Vector2 (currentAngle, currentDistance);
					sw.Write (distances [i].x);
					sw.Write (",");
					sw.WriteLine (distances [i].y);
					msg [4*i] = BitConverter.GetBytes(distances[i].y) [0];
					msg [(4*i)+1] = BitConverter.GetBytes(distances[i].y) [1];
					msg [(4*i)+2] = BitConverter.GetBytes(distances[i].y) [2];
					msg [(4*i)+3] = BitConverter.GetBytes(distances[i].y) [3];
				} else {
					Debug.LogError ("There isn't an object in front of me. What is going on.");
				}

				//increment pointOfOrigin's angle rotation by increment amount
				Vector3 settingAngleVector = pointOfOrigin.localEulerAngles;
				currentAngle = currentAngle + angleIncrement;
				settingAngleVector.y = currentAngle;
				pointOfOrigin.localEulerAngles = settingAngleVector;
			}

			dataSenderOne.Send (msg);
			dataSenderTwo.Send (msg);
				
		}

	}

	void OnApplicationQuit() {
		var fileName = "Frame.txt";

		using (StreamWriter sw = new StreamWriter (fileName)) {
			sw.WriteLine ("END");
		}

		String stop = "STOP";
		byte[] msg = Encoding.ASCII.GetBytes (stop);
		dataSenderTwo.Send (msg);

	}

}
