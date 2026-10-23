import { Injectable, inject, OnInit } from "@angular/core";
import { CanActivate, Router } from "@angular/router";
import { Storage } from '@ionic/storage-angular';

@Injectable({
    providedIn:"root"
})

export class AuthGuard implements CanActivate, OnInit{
    private storage = inject(Storage)

    constructor(
        private router:Router
    ){

    }


      ngOnInit() {
            if (!this.storage || null){
            this.storage.create(); 
        }
  }
    
    async canActivate() : Promise<boolean>{

        const token = await this.storage.get('token');


        if (token){
            return true;
        }else{
            this.router.navigate(['/login']);
            return false;
        }
    }
}