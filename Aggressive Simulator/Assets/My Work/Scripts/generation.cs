using UnityEngine;
using System.Collections.Generic;
using System;

public class generation : MonoBehaviour {
	List<GameObject> objectList = new List<GameObject>();

	void Awake(){
		print ("awaken");
		for (int i = -250; i < 250; i=i+12) {
			for (int j = -250; j < 250; j=j+12) {
				GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
				cube.transform.position = new Vector3(i, 100, j);
				cube.transform.localScale = new Vector3 (10, 10, 10);
				objectList.Add(cube);
			}
		}
	}

	void Start () {
		print ("started fresh memes");
		System.Random rnd = new System.Random ();
		for (int i = 0; i < objectList.Count; i++) {
			int chance = rnd.Next (0,5);
			if (chance == 1) {
				print (i);
				GameObject theObject = objectList [i];
				float x = theObject.transform.position.x;
				float z = theObject.transform.position.z;
				theObject.transform.position = new Vector3 (x, 1, z);
			}
		}
	}

	// Update is called once per frame
}