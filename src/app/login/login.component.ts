import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { v4 as uuidv4 } from 'uuid';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { CommunicationService } from '../services/communication.service/communication.service';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private http: HttpClient, private _snackBar: MatSnackBar, private data: CommunicationService, private router: Router) { }

  // txt = uuidv4();
  hide = true;
  url = 'https://investing-82e20-default-rtdb.firebaseio.com/investing/'
  signlog = "";
  password = "";
  username = "";
  users: String[]=[];
  objs: any[]=[]

  ngOnInit(): void {
    this.http.get(this.url + 'users.json').subscribe((responseData:any) => {
      Object.keys(responseData).forEach(element => {
        this.users.push(responseData[element].user);
        this.objs.push(responseData[element]);
      });
    });
  }

  onConfirm(){
    let txt = uuidv4();
    let userExists = []
    let objExists: any[]=[]
    let passwordInput: string=""

    userExists = this.users.filter(el => {
      return el == this.username
    })
    // console.log("users: ",userExists)
    if(this.signlog=="signup"){
      if (userExists.length==0) {
        let auth = {user: this.username,password: this.password,id:txt}
        this.http.post(this.url+'users.json',auth).subscribe(
          (responseData) => {
            this.updateUsername()
            console.log("New user added");
            this.router.navigateByUrl('/home');
            this.http.put(this.url+'visibility/'+this.username+'.json',{user:this.username}).subscribe()
          },
          (error) => {
            console.log("Error: ",error)
          });
      } else {
        console.log("User already exists!")
        this.openSnackBar("Utente già esistente!")
      }
    } else if (this.signlog=="login") {
        if (userExists.length==0){
          console.log("User does not exist!")
          this.openSnackBar("Utente non esistente!")
        } else {
          objExists = this.objs.filter(el => {
            return el.user == this.username
          })
          console.log("objexists: "+objExists)
          passwordInput = objExists[0].password
          if (passwordInput==this.password){
            this.updateUsername()
            console.log("Welcome back user "+this.username+"!")
            this.router.navigateByUrl('/home');
          } else {
            console.log("Incorrect password!")
            this.openSnackBar("Password errata!")
          }
        }
    }
  }

  openSnackBar(message: string) {
    this._snackBar.open(message, "", {
      duration: 2000
    });
  }

  updateUsername(){
    this.data.changeMessage(this.username)
    // this.data.currentMessage.subscribe(message => console.log("message: "+message))
  }

}
