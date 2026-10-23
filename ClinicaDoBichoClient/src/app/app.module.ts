import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouteReuseStrategy } from '@angular/router';
import { provideIonicAngular, IonicRouteStrategy } from '@ionic/angular';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { Storage } from '@ionic/storage-angular';


@NgModule({

  declarations:[AppComponent],
  imports: [BrowserModule, AppRoutingModule],
  providers: [

    { provide: RouteReuseStrategy, useClass: IonicRouteStrategy },
    provideIonicAngular(),
    Storage,
  ],
  bootstrap: [AppComponent] 
})
export class AppModule {}
