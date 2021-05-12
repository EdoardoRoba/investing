import { HttpClient } from '@angular/common/http';
import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-dialog',
  templateUrl: './dialog.component.html',
  styleUrls: ['./dialog.component.css']
})
export class DialogComponent implements OnInit {

  name = ""
  acronym = ""
  quantity = new Number()
  date = new Date()
  toAdd: any
  starting_price = new Number()
  url = "https://investing-82e20-default-rtdb.firebaseio.com/investing/"

  constructor(private http: HttpClient,@Inject(MAT_DIALOG_DATA) public user: any, private _snackBar: MatSnackBar) { }

  ngOnInit(): void {
  }

  addCrypto(){
    this.toAdd = {user:this.user,name: this.name,acronym:this.acronym,quantity:this.quantity,date:this.date,starting_price:this.starting_price}
    this.http.post(this.url+'visibility/'+this.user+'.json',this.toAdd).subscribe(
      (data) => {
        this.openSnackBar("Crypto added!")
      },
      (error) => {
        console.log("Error: ",error)
        this.openSnackBar("Could not upload the crypto. Try again.")
      });
  }

  openSnackBar(message: string) {
    this._snackBar.open(message, "", {
      duration: 2000
    });
  }

}
