import { Image } from "./image";
import React from "react";

export const Gallery = (props) => {
  return (
    <section id="portfolio" className="text-center">
      <div className="container">
        <div className="section-title">
          <h2>Portafolio de Proyectos Digitales</h2>
          <p>
            Una muestra de casos de éxito donde hemos transformado ideas en plataformas robustas y escalables.
          </p>
        </div>
        <div className="row">
          <div className="portfolio-items">
            {props.data
              ? props.data.map((d, i) => (
                  <div
                    key={`${d.title}-${i}`}
                    className="col-sm-6 col-md-4 col-lg-4"
                  >
                    <Image
                      title={d.title}
                      largeImage={d.largeImage}
                      smallImage={d.smallImage}
                    />
                  </div>
                ))
              : "Loading..."}
          </div>
        </div>
      </div>
    </div>
  );
};
