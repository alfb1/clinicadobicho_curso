import { Component, OnInit, inject, signal } from '@angular/core';
//import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Storage } from '@ionic/storage-angular';
import { IonContent, IonHeader, IonTitle, IonItem, IonLabel, IonInput,
         IonToolbar, IonButton } from '@ionic/angular';
import { ApiService } from '../services/api.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports:[FormsModule, IonInput, IonButton, IonItem, IonLabel, 
           IonContent, IonHeader, IonTitle, IonToolbar ],
  //providers: [
  //  Storage,
  //],
})

export class LoginPage implements OnInit {
  username = signal('');
  password = signal('');
  private storage:Storage = inject(Storage)
  constructor(
    private api: ApiService,
    private router: Router
  ) { }

  ngOnInit() {
    this.storage.create();
  }

  login(){
    this.api.login(this.username(), this.password())
            .subscribe( 
            response =>{
              if (response.access){
                this.storage.set('token', response.access)
                            .then(()=>{
                              this.router.navigate(['/consultas']);
                            });
                }
            },
            err=>{
                 console.error("Erro no login : ", err);
                 alert("Usuário ou senha inválidos!");
              }
            )
  }

}
