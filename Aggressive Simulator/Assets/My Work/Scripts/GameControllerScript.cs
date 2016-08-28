using UnityEngine;
using System.Collections;
using UnityEngine.UI;

public class GameControllerScript : MonoBehaviour {

    public Text ModeText; //tells user what mode the user is driving in

    public int specificCourseSelectionNumber; //every course corresponds to a number in the array. If there is a number for this variable, then the course selection isn't random. 
    public GameObject[] fieldObstacles; //holds all the obstacle objects to disperse in a randomized field
    public GameObject[] courseObjects; //holds an array of all courses - not randomly generated

    public int objectDensity;
    public GameObject parentOfObstacles;

    void Start () {
        GenerateCourse();
    }


    public void GenerateField () {
        int totalFieldObstacleVariations = fieldObstacles.Length;

        for (int i = 0; i <= objectDensity; i++) {
            GameObject go = Instantiate(fieldObstacles[Random.Range(0, totalFieldObstacleVariations)], new Vector3(0, 0, 0), Quaternion.identity) as GameObject;
            //go.transform.eulerAngles.y = Random.Range(0, 360); // this is to set the object to a random rotation for true randomization
            go.name = "Field Obstacle";
            go.transform.parent = parentOfObstacles.transform;
        }
        //UNFINSIHED

        ModeText.text = "Field";
    }

    public void GenerateCourse () {
        if (GameObject.Find("Course") != null) {
            Destroy(GameObject.Find("Course"));
        }

        GameObject go = Instantiate(courseObjects[Random.Range(0, courseObjects.Length)], new Vector3(0, 0, 0), Quaternion.identity) as GameObject;
        go.name = "Course";
        go.transform.parent = parentOfObstacles.transform;
        ModeText.text = "Course";
    }

}
