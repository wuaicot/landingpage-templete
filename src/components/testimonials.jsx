import React from "react";

export const Testimonials = (props) => {
  return (
    <div id="testimonials">
      <div className="container">
        <div className="section-title text-center">
          <h2>Lo que dicen nuestros clientes</h2>
        </div>
        <div className="row" style={{ display: 'flex', flexWrap: 'wrap' }}>
          {props.data
            ? props.data.map((d, i) => (
                <div key={`${d.name}-${i}`} className="col-sm-6 col-md-6 col-lg-4">
                  <div className="testimonial" style={{ marginBottom: '30px', height: '100%' }}>
                    <div className="testimonial-image">
                      {" "}
                      <img src={d.img} alt={d.name} />{" "}
                    </div>
                    <div className="testimonial-content">
                      <p>"{d.text}"</p>
                      <div className="testimonial-meta"> - {d.name} </div>
                    </div>
                  </div>
                </div>
              ))
            : "cargando..."}
        </div>
      </div>
    </div>
  );
};
