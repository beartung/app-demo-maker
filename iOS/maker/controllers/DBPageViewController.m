//
//  DBPageViewController.m
//  maker
//
//  Created by Bear on 2/22/14.
//  Copyright (c) 2014 Bear. All rights reserved.
//

#import "DBPageViewController.h"

@interface DBPageViewController ()

@end

@implementation DBPageViewController

- (id) initWithEnv:(DBEnv *)env pageId:(NSString *)pid referPageId:(NSString *)refer touchHandler:(id<DBTouchControl>)delegate{

    self = [super init];
    self.env = env;
    self.pid = pid;
    self.refer = refer;
    
    DBPage * page = [self.env getPage:self.pid];
    
    NSLog(@"PageViewController init pid=%@, type=%@", page.id, page.type);
    NSLog(@"page rect: %f, %f, %f, %f",
          page.rect.origin.x, page.rect.origin.y, page.rect.size.width, page.rect.size.height);
    DBPageView * pv = [[DBPageView alloc] initWithFrame:page.rect andPage:page referId:refer touchHandler:delegate];
    
    self.page = page;
    self.view = pv;
    self.handler = delegate;
    
    for (int i = 0; i < self.page.subPageIds.count; i++) {
        DBPage * sp = [self.env getPage:self.page.subPageIds[i]];
        if ([sp.type isEqualToString:PAGE_TYPE_LIST]){
            UITableView * table = [[UITableView alloc] initWithFrame:sp.rect style:UITableViewStylePlain];
            table.delegate = self;
            table.dataSource = self;
            table.tag = [sp.id intValue];
            [self.view addSubview:table];
        }
    }
    return self;
}


- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view.
    NSLog(@"PageViewController viewDidLoad");
    NSLog(@"PageViewController viewDidLoad id=%@, refer=%@", self.pid, self.refer);

}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return 30;
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{

    static NSString * tag = @"list_time";
    /*
    UITableViewCell * cell = [tableView dequeueReusableCellWithIdentifier:tag];
    if (cell == nil){
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:tag];
    }
     */
    
    NSString * pid = [NSString stringWithFormat: @"%d", tableView.tag];
    DBPage * page = [self.env getPage:pid];
    
    UITableViewCell * cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:tag];
    
    NSUInteger row = [indexPath row];
    NSString * iid = page.subPageIds[row % page.subPageIds.count];
    DBPage * item = [self.env getPage:iid];
    if (item && item.photo.length > 0){
        DBPageView * pv = [[DBPageView alloc] initWithFrame:item.rect
                                                    andPage:item referId:self.refer touchHandler:self.handler];
        [cell addSubview:pv];
    }
    return cell;
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
    NSString * pid = [NSString stringWithFormat: @"%d", tableView.tag];
    DBPage * page = [self.env getPage:pid];
    NSUInteger row = [indexPath row];
    NSString * iid = page.subPageIds[row % page.subPageIds.count];
    DBPage * item = [self.env getPage:iid];
    return item.rect.size.height;
}

@end
