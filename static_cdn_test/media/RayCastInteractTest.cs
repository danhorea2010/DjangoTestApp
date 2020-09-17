using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityStandardAssets.Characters.FirstPerson;

[System.Serializable]
public class MainInput_Ray
{
    public Ray ray = new Ray();
    public RaycastHit hit;
    public bool HittingSomething { get; set; }
}


public class RayCastInteractTest : MonoBehaviour
{
    [SerializeField] float maxDistance = 2.0f;
    [SerializeField] FirstPersonController firstPersonController;
    [SerializeField] float cursorScaleOnHover = 2.0f;
    [SerializeField] bool DEBUG = true;

    private IInteractable currentInteractable;
    private Image cursorImage;

    private Vector2 originalCursorSize;
    private Vector2 scaledCursorSize;

    public MainInput_Ray mainInput_Ray;

    private void Start()
    {
        mainInput_Ray = new MainInput_Ray();
        cursorImage = UI_Controller.instance.GetCursorImage();
        originalCursorSize = cursorImage.rectTransform.sizeDelta;
        scaledCursorSize = new Vector2(1, 1) * cursorImage.rectTransform.sizeDelta * cursorScaleOnHover;

        UI_Controller.instance.OnNoteDone += OnNoteDone;
    }

    private void OnNoteDone()
    {
        firstPersonController.SetCursorLock(true);
        firstPersonController.enabled = true;
    }

    private void Update()
    {
        DoRayCast();

        if (Input.GetMouseButtonDown(0))
        {
            if (currentInteractable != null)
            {
                currentInteractable.Interact();


            }
        }
    }

    void DoRayCast()
    {
        mainInput_Ray.HittingSomething = Physics.Raycast(transform.position, transform.TransformDirection(Vector3.forward), out mainInput_Ray.hit, maxDistance);

        if (mainInput_Ray.HittingSomething)
        {
            currentInteractable = mainInput_Ray.hit.collider.GetComponent<IInteractable>();

            if (DEBUG)
            {
                Debug.DrawRay(transform.position, transform.TransformDirection(Vector3.forward) * maxDistance, Color.green);

            }
        }
        else
        {
            currentInteractable = null;

            if (DEBUG)
            {
                Debug.DrawRay(transform.position, transform.TransformDirection(Vector3.forward) * maxDistance, Color.red);
            }
        }

        if(currentInteractable != null)
        {
            cursorImage.rectTransform.sizeDelta = scaledCursorSize;
            UI_Controller.SetDisplayText(currentInteractable.OnHoverText);
        }
        else
        {
            cursorImage.rectTransform.sizeDelta = originalCursorSize;
            UI_Controller.SetDisplayText("");
        }

    }


}
