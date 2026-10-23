import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common'
import { FormControl, FormGroup, ReactiveFormsModule, FormsModule } from '@angular/forms';
import { IonContent, IonHeader, IonTitle, IonToolbar, IonIcon, IonButton,  IonLabel,
         IonItem, IonSelect, IonSelectOption, IonDatetime, IonTextarea 
 } from '@ionic/angular';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';
import { Consulta } from "../models/Consulta.model";
import { Veterinario } from "../models/Veterinario.model";
import { Animal } from "../models/Animal.model";

@Component({
  selector: 'app-agendar-consulta',
  templateUrl: './agendar-consulta.page.html',
  styleUrls: ['./agendar-consulta.page.scss'],
  standalone: true,
  imports: [ CommonModule, FormsModule, ReactiveFormsModule, IonContent, 
             IonHeader, IonTitle, IonToolbar, IonIcon, IonButton, IonLabel,
             IonItem, IonSelect, IonSelectOption, IonDatetime, IonTextarea ]
})

export class AgendarConsultaPage implements OnInit {

  consulta:Consulta=({} as any) as Consulta;
  animais:Animal[]=[];
  veterinarios:Veterinario[]=[];
  apiService = inject(ApiService); 
  minDate:string = (new Date()).toISOString();
  maxDate:string  = (new Date(new Date().setDate(new Date().getDate() + 30))).toISOString();

  agendarConsultaForm = new FormGroup({
    animal : new FormControl(''),
    data   : new FormControl(''),
    motivo : new FormControl(''),
    veterinario : new FormControl(''),
  })

  constructor(private router:Router) {}

  ngOnInit() {

    this.getAnimais();
    this.getVeterinarios();
  }

  agendar(){
    const dateConsulta = new Date(this.consulta.data || 0) ;
    const hour = dateConsulta.getHours();
    const valid_hours = (hour >= 8 && hour < 12) !! ( hour >= 13 && hour < 17)

    if ( ! valid_hours ){
        alert('Horário deve ser entre 08:00-12:00 e 13:00-17:00');
        return;
    }

    console.log("Consulta a agendar: ", this.consulta);

    this.apiService.agendarConsulta( this.consulta!)
            .subscribe( 
              (data:Consulta) =>{
                     console.log("Status:", data);
                     this.router.navigate(['/consultas']);
              },
              (err:Error) =>{ 
                    console.log("Status:", err);
                    alert('Erro ao agendar!');
              } 
            )
  }

  getAnimais(){
    this.apiService.getAnimais()
                   .subscribe(
                     (animais:Animal[])=>{
                      this.animais = animais;
                      console.log("animais", this.animais);
                     },
                     (err:Error)=>{
                      console.error("Status:", err);
                      alert("error ao ler animais");
                     }
                   )
  }

  getVeterinarios(){
    this.apiService.getVeterinarios()
                   .subscribe(
                    (veterinarios:Veterinario[]) =>{
                      this.veterinarios = veterinarios;
                      console.log(veterinarios);
                    },
                    (err:Error) => {
                      console.error("Status:", err);
                      alert("Erro ao ler veterinarios");
                    }
                   );
  }

}
