//input
//digital input
int ON=13;
//analog input
int ir_ll = A0;// infra red left-left lick
int ir_lr = A1;// infra red left-right lick
int ir_ls = A2;// infra red left-start of context
int ir_rl = A3;// infra red right-left lick
int ir_rr = A4;// infra red right-right lick
int ir_rs = A5;// infra red right-start of context
int ir[6];

int stat = 0;
int Trial_num = 0;
int left_choice = 0;
int right_choice = 0;

void setup() {
  // put your setup code here, to run once:
pinMode(ir_ll,INPUT);int ir_ll_value = 0;
pinMode(ir_lr,INPUT);int ir_lr_value = 0;
pinMode(ir_ls,INPUT);int ir_ls_value = 0;
pinMode(ir_rl,INPUT);int ir_rl_value = 0;
pinMode(ir_rr,INPUT);int ir_rr_value = 0;
pinMode(ir_rs,INPUT);int ir_rs_value = 0;

Serial.begin(9600);
}

float Read_analog(int analog, int times) {
  float sum = 0;
  for (int i = 0; i <= times; i++) {
    int value = analogRead(analog);
    sum = sum + value;
  }
  //Serial.println(sum/times);
  return sum / times;
}

float Read_digital(int digital, int times) {
  float sum = 0;
  for (int i = 0; i <= times; i++) {
    int value = digitalRead(digital);
    sum = sum + value;
  }
  return sum / times;
}

void Read_ir(){
  if (Read_analog(ir_ll,10) < 500){ir[0] = 1;}else{ir[0] = 0;}  
  if (Read_analog(ir_lr,10) < 500){ir[1] = 1;}else{ir[1] = 0;}  
  if (Read_analog(ir_ls,10) < 500){ir[2] = 1;}else{ir[2] = 0;}  
  if (Read_analog(ir_rl,10) < 500){ir[3] = 1;}else{ir[3] = 0;}  
  if (Read_analog(ir_rr,10) < 500){ir[4] = 1;}else{ir[4] = 0;}  
  if (Read_analog(ir_rs,10) < 500){ir[5] = 1;}else{ir[5] = 0;}   
//  Serial.print(Read_analog(ir_ll,10));Serial.print(" ");
//  Serial.print(Read_analog(ir_lr,10));Serial.print(" ");
//  Serial.print(Read_analog(ir_ls,10));Serial.print(" ");
//  Serial.print(Read_analog(ir_rl,10));Serial.print(" ");
//  Serial.print(Read_analog(ir_rr,10));Serial.print(" ");
//  Serial.println(Read_analog(ir_rs,10));  
//  delay(100);
    
}

void loop() {
  
  float on_signal = Read_digital(ON, 10);
  //Serial.print(on_signal);
//  ir[0] ir_ll //as nose poke
//  ir[1] ir_lr //no use
//  ir[2] ir_ls //context enter or reverse_exit
//  ir[3] ir_rl //one of the choice
//  ir[4] ir_rr //one of the choice
//  ir[5] ir_rs // context exit or reverse_enter
  if(on_signal >= 0.90){      
    do{Read_ir();}while(ir[0]==0);  //ir_ll as nose poke
    Serial.println("Stat1: nose poke");
    unsigned long start_trial_time = millis();// means one trial gets started
    Trial_num =Trial_num + 1;       
    do{Read_ir();}while(ir[2]==0);unsigned long context_enter_time = millis();
    Serial.println("Stat2: context enter");
    do{Read_ir();}while(ir[5]==0);unsigned long context_exit_time = millis();
    Serial.println("Stat3: context exit");
    do{Read_ir();}while(ir[3]==0 && ir[4]==0 );unsigned long choice_time = millis();
    Serial.println("Stat4: choice");
    if (ir[3]==1){
      left_choice= left_choice + 1;      
      stat = 1;}
    else if (ir[4]==1){
      right_choice=right_choice + 1;
      stat = 2;} 
    do{Read_ir();}while(ir[5]==0);unsigned long context_reverse_enter_time = millis();
    Serial.println("Stat5: context reverse enter");
    do{Read_ir();}while(ir[2]==0);unsigned long context_reverse_exit_time = millis();
    Serial.println("Stat6: context reverse exit");
    Serial.print("Sum: ");
    Serial.print(Trial_num);
    Serial.print(" ");
      if (stat==1){
        Serial.print("l");
        Serial.print(" ");
        Serial.print(left_choice);
        Serial.print(" ");
      }else if(stat ==2){
        Serial.print("r");
        Serial.print(" ");
        Serial.print(right_choice);
        Serial.print(" ");}
      
    Serial.print(start_trial_time);
    Serial.print(" ");  
    Serial.print(context_enter_time);
    Serial.print(" "); 
    Serial.print(context_exit_time);   
    Serial.print(" "); 
    Serial.print(choice_time); 
    Serial.print(" "); 
    Serial.print(context_reverse_enter_time); 
    Serial.print(" "); 
    Serial.println(context_reverse_exit_time); 
    stat=0;  
  }else{
//    Read_ir();
//    for (int i = 0;i<6;++i){
//    if (i<5){Serial.print(ir[i]);}
//    else{Serial.println(ir[i]);}}
    stat = 0;
    Trial_num = 0;
    left_choice = 0;
    right_choice = 0;}
}
