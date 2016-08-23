using UnityEngine;
using System.Collections;
using System.IO;
using System;

[RequireComponent (typeof (LineRenderer))]
public class LaserSight : MonoBehaviour {

	public float currentDistance = 0;
	public float currentRotation;

	public Transform pointOfOrigin;

	public bool LaserVisible = false;
	private LineRenderer lr;

	public float totalAngleDesired = 270f;
	public float angleIncrement = .5f;

	public Vector2[] distances;
	int totalAngleIncremented; 

	int frameNumber = 0;

	void Start () {
		lr = GetComponent<LineRenderer>();
		SwitchToTurnRight();

		totalAngleIncremented = (int) (totalAngleDesired/ angleIncrement); //i.e: 270 into half angles - 270/.5 = 540
		distances = new Vector2[totalAngleIncremented];
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
			for (int i = 0; i < totalAngleIncremented; i++) {
				//send a raycast at current angle
				if (Physics.Raycast (pointOfOrigin.position, pointOfOrigin.forward, out Hit)) {
					currentDistance = Hit.distance;
					//assign distance to the Vector2 list:
					distances [i] = new Vector2 (currentAngle, currentDistance);
					sw.Write (distances [i].x);
					sw.Write (",");
					sw.WriteLine (distances [i].y);
				} else {
					Debug.LogError ("There isn't an object in front of me. What is going on.");
				}

				//increment pointOfOrigin's angle rotation by increment amount
				Vector3 settingAngleVector = pointOfOrigin.localEulerAngles;
				currentAngle = currentAngle + angleIncrement;
				settingAngleVector.y = currentAngle;
				pointOfOrigin.localEulerAngles = settingAngleVector;
			}
		}

	}

	void SwitchToTurnRight() {
		//start collecting lidar data
	}

}
