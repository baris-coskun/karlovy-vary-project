// İçerikler (Tamamen Lorem Ipsum)
const pages = {
  spa: `
          <div class="landmarks-hero spa-bg"></div>
      <h2 class="landmarks-heading">Spa Sights</h2>
      <p class="landmarks-text">
           Karlovy Vary is internationally known for its spa tradition and
            natural mineral springs. The spa sights represent the historical and
            cultural heart of the city, attracting visitors for centuries
            because of their healing properties and unique architecture.
      </p>
      <div class="sub-block">
        <h3>Hot Springs</h3>
        <p>             The hot springs of Karlovy Vary are the most important natural
              phenomenon of the city. Thermal water rises from deep underground
              and is traditionally used for drinking treatments and spa
              therapies..</p>
      </div>
      <div class="sub-block">
        <h3>Colonnades</h3>
        <p> The colonnades serve as elegant shelters for the mineral springs.
              They are characteristic architectural structures that combine
              functionality with artistic design and are among the most
              photographed landmarks in the city.</p>
      </div>
      <div class="sub-block">
        <h3>Spa Architecture</h3>
        <p> Many spa buildings were constructed in the 18th and 19th
              centuries. These buildings reflect classical and neo-renaissance
              styles, creating a distinctive atmosphere that connects health,
              culture, and history.</p>
      </div>
    `,

  church: `
  <div class="landmarks-hero church-bg"></div>
      <h2 class="landmarks-heading">Church Monuments</h2>
      <p class="landmarks-text">
    Church monuments in Karlovy Vary reflect the religious diversity and historical development of the region.
They are significant not only as places of worship but also as architectural and cultural monuments.
      </p>
      <div class="sub-block">
        <h3>Historic Churches</h3>
        <p>Several churches in the city date back to the 18th century.
Their interiors often feature rich decorations, sculptures, and paintings representing religious traditions..</p>
      </div>
      <div class="sub-block">
        <h3>Sacral Architecture</h3>
        <p>Church buildings demonstrate a variety of architectural styles.
Baroque and neo-Gothic elements are commonly found, emphasizing vertical structures and decorative facades.</p>
      </div>
      <div class="sub-block">
        <h3>Cultural Importance</h3>
        <p>Church monuments play an important role in local traditions and celebrations.
They serve as places for community gatherings, concerts, and cultural events.</p>
      </div>
    `,

  towers: `
  <div class="landmarks-hero towers-bg"></div>
      <h2 class="landmarks-heading">Towers & Viewpoints</h2>
      <p class="landmarks-text">
The towers and viewpoints of Karlovy Vary offer panoramic views of the city and surrounding forests.
These landmarks are popular tourist destinations and highlight the natural beauty of the region.
      </p>
      <div class="sub-block">
        <h3>Observation Towers</h3>
        <p>Observation towers allow visitors to view the city from elevated positions.
They were often built for tourism and recreation purposes and remain popular sightseeing spots.</p>
      </div>
      <div class="sub-block">
        <h3>Scenic Viewpoints</h3>
        <p>Natural viewpoints are located along forest paths and hills.
They provide peaceful places to admire the spa town landscape and take photographs.</p>
      </div>
      <div class="sub-block">
        <h3>Tourist Routes</h3>
        <p>Many towers and viewpoints are connected by walking and hiking routes.
These paths combine physical activity with sightseeing and nature exploration.</p>
      </div>
    `,

  protected: `
  <div class="landmarks-hero protected-bg"></div>
      <h2 class="landmarks-heading">Protected Buildings</h2>
      <p class="landmarks-text">
 Protected buildings represent the architectural and historical heritage of Karlovy Vary.
They are legally preserved to maintain the city’s cultural identity for future generations.
      </p>
      <div class="sub-block">
        <h3>Historical Villas</h3>
        <p>Many villas were originally built as residences for wealthy spa guests.
They showcase elegant designs, decorative facades, and distinctive materials.</p>
      </div>
      <div class="sub-block">
        <h3>Preservation Efforts</h3>
        <p>Strict regulations ensure that protected buildings are properly maintained.
Restoration projects aim to preserve original details while adapting buildings for modern use.</p>
      </div>
      <div class="sub-block">
        <h3>Cultural Heritage</h3>
        <p>Protected buildings help tell the story of the city’s past.
They connect architectural beauty with social and historical significance.</p>
      </div>
    `,
};

const menuLinks = document.querySelectorAll(".side-menu a");
const contentArea = document.getElementById("content-area");

menuLinks.forEach((link) => {
  link.addEventListener("click", () => {
    // Menü aktifliğini değiştir
    menuLinks.forEach((l) => l.classList.remove("active"));
    link.classList.add("active");

    // İçeriği değiştir
    const page = link.getAttribute("data-page");
    contentArea.innerHTML = pages[page];
  });
});
