package com.example.keypadlockapp;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatDialogFragment;

public class passcodeDialog extends AppCompatDialogFragment {
    private EditText editTextPasscode;
    private passcodeDialogListener listener;
    private static final String TAG = "passcodeDialog";
    @NonNull
    @Override
    public Dialog onCreateDialog(@Nullable Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater inflater = getActivity().getLayoutInflater();
        View view = inflater.inflate(R.layout.layout_dialog,null);
        builder.setView(view) //this creates the dialog box
                .setTitle("Set Passcode to 0000 to disable")
                .setNegativeButton("cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                    }
                })
                .setPositiveButton("ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String passcode = editTextPasscode.getText().toString();
                        System.out.println("passcode recieved is: "+passcode);  //code for testing purposes
                        Log.i(TAG,"passcode recieved is: "+passcode); //code for testing purposes
                        listener.applytext(passcode); //calls back to the ActivityMain class to update the information
                    }
                });
    editTextPasscode = view.findViewById(R.id.edit_passcode);
        return builder.create();
    }

    @Override
    public void onAttach(@NonNull Context context) {
        super.onAttach(context);
        try {
            listener = (passcodeDialogListener) context;
        } catch (ClassCastException e) {
            throw new ClassCastException(context.toString() +
                    "must implement ExampleDialogListener");
        }
    }

    public interface passcodeDialogListener{
        void applytext(String pascode);
    }
}
