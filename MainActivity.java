package com.example.keypadlockapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class MainActivity extends AppCompatActivity implements  passcodeDialog.passcodeDialogListener{
    private TextView mainPasscode;
    private TextView tempPasscode;
    private TextView gateStatusText;
    private Button btnTempPasscode;
    private Button btnMainPasscode;
    private Button btnOpenGate;
    private Button btnCloseGate;
    private ImageView imageViewGateStatus;

    private boolean mainselected = false;
    final String httpPath = "http://192.168.0.120:8080/";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mainPasscode = (TextView) findViewById(R.id.mainPasscode);
        tempPasscode = (TextView) findViewById(R.id.tempPasscode);
        gateStatusText = (TextView) findViewById(R.id.gateStatusText);
        btnTempPasscode = (Button) findViewById(R.id.btnTempPasscode);
        btnMainPasscode = (Button) findViewById(R.id.btnMainPasscode);
        btnOpenGate = (Button) findViewById(R.id.btnOpenGate);
        btnCloseGate = (Button) findViewById(R.id.btnCloseGate);
        imageViewGateStatus = (ImageView) findViewById(R.id.imageView_gateStatus);

        btnTempPasscode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mainselected = false;
                openDialog();
            }
        });
        btnMainPasscode.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                mainselected = true;
                openDialog();
            }
        });
        btnOpenGate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                imageViewGateStatus.setImageResource(android.R.drawable.button_onoff_indicator_off);
                gateStatusText.setText("Open");
                //call the method that posts to the https
                openWeb("off");
            }
        });
        btnCloseGate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                gateStatusText.setText("Closed");
                imageViewGateStatus.setImageResource(android.R.drawable.button_onoff_indicator_on);
                //call the method that posts to the https
                openWeb("on");
            }
        });
        // ATTENTION: This was auto-generated to handle app links.
        Intent appLinkIntent = getIntent();
        String appLinkAction = appLinkIntent.getAction();
        Uri appLinkData = appLinkIntent.getData();
    }
    public void openDialog(){
        //opens the enter number dialog
        passcodeDialog passcodeDialog = new passcodeDialog();
        passcodeDialog.show(getSupportFragmentManager(), "Passcode dialog");

    }
    public void openWeb(String postMessage){
        WebView webView = new WebView(this);
        //setContentView(webView);  //this is the code to display the webpage, which i dont want to do
        webView.loadUrl(httpPath+postMessage);
    }
    public void sendPost(String postMessage){ //code not used, doesn't work
        OkHttpClient client = new OkHttpClient();

        String url = "http://192.168.0.120:8080/";

        Request request = new Request.Builder()
                .url(url)
                .build();
        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if(response.isSuccessful()){
                    final String myResponse = response.body().string();

                    MainActivity.this.runOnUiThread((new Runnable() {
                        @Override
                        public void run() {
                            tempPasscode.setText(myResponse);
                        }
                    }));
                }

            }
        });
        //THE FOLLOWING CODE DOESN'T WORK BECAUSE IT WAS DEPRECATED
//        HttpClient httpClient = new DefaultHttpClient();
//        HttpGet httpGet = new HttpGet(httpPath);
//        try {
//            HttpEntity httpEntity = httpClien.execute(httpGet).getEntity();
//            if (httpEntity != null){
//                InputStream inputStream = httpEntity.getContent();
//                BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));
//                StringBuilder stringBuilder = new StringBuilder();
//                String line = null;
//
//                while((line=bufferedReader.readLine()) !=null){
//                    stringBuilder.append(line+"n");
//                }
//                inputStream.close();
//                tempPasscode.setText(stringBuilder.toString());
//            }
//        }
//        catch (ClientProtocolException e){
//            e.printStackTrace();
//            Toast.makeText(HTTPMethodsActivity.this,e.toString(),Toast.LENGTH_LONG);
//        }
//        catch (IOException e){
//            e.printStackTrace();
//            Toast.makeText(HTTPMethodsActivity.this,e.toString(),Toast.LENGTH_LONG);
//        }
    }

    @Override
    public void applytext(String passcode) {
        System.out.println("passcode to  text is: "+passcode);
        if (mainselected){
            mainPasscode.setText(passcode);
            //call the method that posts to the https
            openWeb("setTemp_"+passcode);
        }
        else{
            tempPasscode.setText(passcode);
            //call the method that posts to the https
            openWeb("setMain_"+passcode);
        }
        mainselected = false;
    }
}